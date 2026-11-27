import { useState, useSyncExternalStore } from 'react'

export const defaultChartFrameRate = 30
export type ChartFrameRate = 'native' | typeof defaultChartFrameRate

const cappedFrameInterval = 1000 / defaultChartFrameRate
const motionQuery = '(prefers-reduced-motion: reduce)'

type Frame = {
  step: (now: number) => boolean
  onError: (error: unknown) => void
}

function createChartClock() {
  const frames = new Set<Frame>()
  let pending: number | undefined

  function tick(now: number) {
    pending = undefined
    for (const frame of frames) {
      try {
        if (!frame.step(now)) frames.delete(frame)
      } catch (error) {
        frames.delete(frame)
        try {
          frame.onError(error)
        } catch (handlingError) {
          reportError(handlingError)
        }
      }
    }
    if (frames.size) pending = requestAnimationFrame(tick)
  }

  return (step: Frame['step'], onError: Frame['onError']) => {
    const frame = { step, onError }
    frames.add(frame)
    if (pending === undefined) pending = requestAnimationFrame(tick)
    return () => {
      frames.delete(frame)
      if (!frames.size && pending !== undefined) {
        cancelAnimationFrame(pending)
        pending = undefined
      }
    }
  }
}

export type ChartClock = ReturnType<typeof createChartClock>

export function useChartClock() {
  return useState(createChartClock)[0]
}

function subscribeToMotion(notify: () => void) {
  const preference = window.matchMedia(motionQuery)
  preference.addEventListener('change', notify)
  document.addEventListener('visibilitychange', notify)
  return () => {
    preference.removeEventListener('change', notify)
    document.removeEventListener('visibilitychange', notify)
  }
}

export function canAnimateCharts() {
  return document.visibilityState === 'visible' && !window.matchMedia(motionQuery).matches
}

export function useChartMotionPreference() {
  return useSyncExternalStore(subscribeToMotion, canAnimateCharts, () => false)
}

export function chartMotionProgress(elapsed: number, duration: number, delay = 0) {
  return Math.min(1, Math.max(0, (elapsed - delay) / duration))
}

type ChartMotionTiming = {
  duration: number
  delay: number
  firstSample: boolean
  rate: ChartFrameRate
  isEnabled: () => boolean
}

export function playChartMotion(
  clock: ChartClock,
  { duration, delay, firstSample, rate, isEnabled }: ChartMotionTiming,
  paint: (elapsed: number, finished: boolean) => void,
  onError: Frame['onError'],
) {
  const start = performance.now()
  const interval = cappedFrameInterval - .25
  let lastPaint = firstSample ? -Infinity : start

  return clock((now) => {
    const elapsed = now - start
    const finished = elapsed >= duration || !isEnabled() || document.visibilityState !== 'visible'
    // Leave room for the exact final paint without delaying the end of the animation.
    const hold = rate === defaultChartFrameRate && (now - lastPaint < interval || duration - elapsed < interval)
    if (!finished && (elapsed < delay || hold)) return true
    lastPaint = now
    paint(finished ? duration : Math.max(0, elapsed), finished)
    return !finished
  }, onError)
}

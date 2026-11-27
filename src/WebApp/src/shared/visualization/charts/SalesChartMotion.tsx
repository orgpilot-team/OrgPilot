import type { BarSeriesOption, LineSeriesOption } from 'echarts/charts'
import type { EChartsType } from 'echarts/core'
import { createContext, useCallback, useContext, useLayoutEffect, useMemo, useRef } from 'react'
import type { PropsWithChildren } from 'react'
import type { ChartConnection } from './ChartHost'
import { canAnimateCharts, chartMotionProgress, defaultChartFrameRate, playChartMotion, useChartClock, useChartMotionPreference } from './chart-motion'
import type { ChartClock, ChartFrameRate } from './chart-motion'
import type { ChartOption } from './echarts-runtime'
import type { TrendFrame, TrendValues } from './luminous-sales-trend'
import type { SalesChartAnimation, TrendObservation } from './SalesChartPresentation'

const ChartClockContext = createContext<ChartClock | null>(null)

/** Let charts in the same view share a clock. Each chart also works on its own. */
export function ChartMotionGroup({ children }: PropsWithChildren) {
  const clock = useChartClock()
  return <ChartClockContext.Provider value={clock}>{children}</ChartClockContext.Provider>
}

export function useSalesChartAnimation(luminous: boolean, animation?: SalesChartAnimation) {
  const preference = useChartMotionPreference()
  return {
    enabled: luminous && (animation?.enabled ?? true) && preference,
    frameRate: animation?.frameRate ?? defaultChartFrameRate,
    replay: animation?.replayKey ?? 0,
  }
}

const trendDuration = 900
const branchDelay = 120
const branchDuration = 700
const barStagger = 90
const updateDuration = 450

type TrendMotion = {
  rows: readonly TrendObservation[]
  accepted: TrendValues
  frame: TrendFrame
}

type ChartMotionRequest = {
  option: ChartOption
  identity: string
  structure: string
  replay: number
  enabled: boolean
  frameRate: ChartFrameRate
  trend?: TrendMotion
}

function withSelection(option: ChartOption, selection?: ChartOption): ChartOption {
  const legend = Array.isArray(option.legend) ? option.legend[0] : option.legend
  const oldLegend = Array.isArray(selection?.legend) ? selection.legend[0] : selection?.legend
  if (legend && oldLegend?.selected) return { ...option, legend: { ...legend, selected: oldLegend.selected } }

  const bar = Array.isArray(option.series) ? option.series[0] : option.series
  const oldBar = Array.isArray(selection?.series) ? selection.series[0] : selection?.series
  if (bar?.type === 'bar' && oldBar?.type === 'bar' && oldBar.selectedMap) {
    return { ...option, series: [{ ...bar, selectedMap: oldBar.selectedMap }] }
  }
  return option
}

function blend(from: TrendValues, to: TrendValues, progress: number): TrendValues {
  function interpolate(before: (number | null)[], after: (number | null)[]) {
    return after.map((value, index) => {
      const start = before[index]
      return start === null || value === null ? value : start * (1 - progress) + value * progress
    })
  }
  return { current: interpolate(from.current, to.current), previous: interpolate(from.previous, to.previous) }
}

export function trendAnomalyPoints(rows: readonly TrendObservation[], values: (number | null)[], reached = (_index: number) => true) {
  return rows.flatMap(({ anomaly }, index) => {
    const value = values[index]
    return anomaly && value !== null && reached(index) ? [{ name: anomaly, coord: [index, value] }] : []
  })
}

function trendSeries(trend: TrendMotion) {
  const values = trend.frame.values ?? trend.accepted
  const reveal = trend.frame.reveal
  const last = Math.max(1, trend.rows.length - 1)
  const reached = (index: number) => (trend.rows.length === 1 ? .5 : index / last) <= reveal
  const current: LineSeriesOption = {
    id: 'current',
    type: 'line',
    data: values.current,
    symbolSize: reveal >= 1 ? 8 : (_value, point) => reached(point.dataIndex) ? 8 : 0,
    markPoint: {
      data: trendAnomalyPoints(trend.rows, values.current, reached),
    },
  }
  const previous: LineSeriesOption = {
    id: 'previous',
    type: 'line',
    data: values.previous,
    symbolSize: reveal >= 1 ? 5 : (_value, point) => reached(point.dataIndex) ? 5 : 0,
  }
  return [current, previous]
}

function cubicOut(progress: number) {
  return 1 - (1 - progress) ** 3
}

function applyTrendFrame(option: ChartOption, trend: TrendMotion): ChartOption {
  const frame = trendSeries(trend)
  const series = Array.isArray(option.series) ? option.series : [option.series]
  return {
    ...option,
    series: series.flatMap((item) => {
      if (!item) return []
      const patch = item.type === 'line' && frame.find(({ id }) => id === item.id)
      return patch && item.type === 'line'
        ? [{ ...item, ...patch, markPoint: item.markPoint && { ...item.markPoint, ...patch.markPoint } }]
        : [item]
    }),
  }
}

function getBar(option: ChartOption) {
  const series = Array.isArray(option.series) ? option.series[0] : option.series
  return series?.type === 'bar' ? series : undefined
}

function getStagger(bar: BarSeriesOption) {
  return (bar.data?.length ?? 0) > 1 ? barStagger : 0
}

function barAnimation(option: ChartOption, bar: BarSeriesOption, entrance: boolean): ChartOption {
  const stagger = getStagger(bar)
  const last = Math.max(1, (bar.data?.length ?? 0) - 1)
  return {
    ...option,
    animation: true,
    animationEasing: 'cubicOut',
    animationEasingUpdate: 'cubicOut',
    animationDuration: branchDuration - stagger,
    animationDurationUpdate: updateDuration,
    animationDelay: entrance ? (index: number) => branchDelay + stagger * index / last : 0,
    animationDelayUpdate: 0,
    series: [{ ...bar, markLine: { ...bar.markLine, animation: false } }],
  }
}

function barFrame(bar: BarSeriesOption, elapsed: number, from?: BarSeriesOption['data']) {
  const stagger = getStagger(bar)
  return bar.data?.map((item, index, all) => {
    if (!item || typeof item !== 'object' || !('value' in item) || typeof item.value !== 'number') return item
    const before = from?.[index]
    const earlier = before && typeof before === 'object' && 'value' in before ? before : undefined
    const start = typeof earlier?.value === 'number' ? earlier.value : 0
    const delay = from ? 0 : branchDelay + stagger * index / Math.max(1, all.length - 1)
    const duration = from ? updateDuration : branchDuration - stagger
    const progress = chartMotionProgress(elapsed, duration, delay)
    if (progress === 1) return item
    const value = start + (item.value - start) * cubicOut(progress)
    const appearance = (value < 0) === (item.value < 0) ? item : earlier ?? item
    return { ...item, value, itemStyle: appearance.itemStyle }
  })
}

export function useSalesChartMotion(request: ChartMotionRequest) {
  const groupClock = useContext(ChartClockContext)
  const ownClock = useChartClock()
  const clock = groupClock ?? ownClock
  const latest = useRef(request)
  const presented = useRef(false)
  const lastReplay = useRef(request.replay)
  const saved = useRef<ChartOption | undefined>(undefined)
  useLayoutEffect(() => { latest.current = request }, [request])

  const connect = useCallback((chart: EChartsType, reportFailure: () => void): ChartConnection => {
    let previous: ChartMotionRequest | undefined
    let cancelFrame: (() => void) | undefined
    let renderedBars: BarSeriesOption['data']
    let wasAnimated = false

    function cancel() {
      cancelFrame?.()
      cancelFrame = undefined
    }

    function play(duration: number, delay: number, firstSample: boolean, paint: (elapsed: number, finished: boolean) => void) {
      cancelFrame = playChartMotion(clock, {
        duration, delay, firstSample,
        rate: latest.current.frameRate,
        isEnabled: () => latest.current.enabled,
      }, (elapsed, finished) => {
        paint(elapsed, finished)
        if (finished) cancelFrame = undefined
      }, () => {
        cancelFrame = undefined
        reportFailure()
      })
    }

    return {
      setOption(option) {
        const next = latest.current
        const replay = next.replay !== lastReplay.current
        const animate = next.enabled && canAnimateCharts()
        const stopMotion = wasAnimated && !animate
        wasAnimated = animate
        const compatible = previous?.structure === next.structure
        const changed = previous?.identity !== next.identity || !compatible
        const modeChanged = previous && previous.frameRate !== next.frameRate
        const entrance = animate && (!presented.current || replay)
        const update = animate && !entrance && !modeChanged && Boolean(previous && changed && compatible)
        const from = previous?.trend?.frame.values ?? previous?.trend?.accepted
        const revealFrom = previous?.trend?.frame.reveal ?? 1
        const trend = next.trend

        lastReplay.current = next.replay
        presented.current = true
        if (previous && !changed && !replay && !stopMotion && !modeChanged) return

        cancel()
        if (changed && previous) chart.dispatchAction({ type: 'hideTip' })
        const replace = !previous || entrance || !compatible || !animate || Boolean(modeChanged)
        const selection = previous ? chart.getOption() as ChartOption : saved.current
        previous = next
        const selected = withSelection(option, selection)

        if (!trend) {
          if (!animate || replace) chart.getZr().animation.clear()
          const bar = getBar(selected)
          if (bar && next.frameRate === defaultChartFrameRate && (entrance || update)) {
            const before = update ? renderedBars : undefined
            renderedBars = barFrame(bar, 0, before)
            chart.setOption({ ...selected, series: [{ ...bar, data: renderedBars }] }, { notMerge: replace, silent: true })
            play(entrance ? branchDelay + branchDuration : updateDuration, entrance ? branchDelay : 0, false, (elapsed, finished) => {
              renderedBars = finished ? bar.data : barFrame(bar, elapsed, before)
              chart.setOption({ series: [{ id: bar.id, type: 'bar', data: renderedBars }] }, { silent: true })
            })
            return
          }
          if (entrance && selection && bar) {
            // ECharts can reuse the bar view across a replacement. Empty its item list before replay.
            chart.setOption({ animation: false, series: [{ id: 'branch-sales', data: [] }] }, { silent: true })
          }
          renderedBars = bar?.data
          const animated = bar && (entrance || update) ? barAnimation(selected, bar, entrance) : selected
          chart.setOption(animated, { notMerge: replace, silent: true })
          return
        }

        trend.frame.values = update ? from : undefined
        trend.frame.reveal = entrance ? 0 : update ? revealFrom : 1
        chart.setOption(entrance || update ? applyTrendFrame(selected, trend) : selected, { notMerge: replace, silent: true })
        if (!entrance && !update) return

        const duration = entrance ? trendDuration : updateDuration
        const startReveal = entrance ? 0 : revealFrom
        play(duration, 0, entrance, (elapsed, finished) => {
          const t = chartMotionProgress(elapsed, duration)
          const progress = entrance ? t * (2 - t) : cubicOut(t)
          trend.frame.reveal = finished ? 1 : startReveal + (1 - startReveal) * progress
          trend.frame.values = !finished && update && from ? blend(from, trend.accepted, progress) : undefined
          chart.setOption({ series: trendSeries(trend) }, { silent: true })
        })
      },
      dispose() {
        cancel()
        if (previous) {
          const option = chart.getOption() as ChartOption
          const legend = Array.isArray(option.legend) ? option.legend[0] : option.legend
          const series = Array.isArray(option.series) ? option.series[0] : option.series
          saved.current = {
            legend: legend && { selected: legend.selected },
            series: series?.type === 'bar' ? [{ type: 'bar', selectedMap: series.selectedMap }] : undefined,
          }
        }
      },
    }
  }, [clock])

  // Replay and motion preference changes use the same host update entry point as data changes.
  const option = useMemo(() => ({ ...request.option }), [request])
  return { connect, option }
}

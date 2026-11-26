import { init } from 'echarts/core'
import type { EChartsType, SelectChangedEvent } from 'echarts/core'
import type { LegendComponentOption } from 'echarts/components'
import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { PanelState } from '../../design-system/patterns/PanelState'
import { useDidrahTheme } from '../../design-system/theme/DidrahThemeProvider'
import { chartCanvasFont, chartThemes, chartTooltipFont } from './chart-theme'
import './echarts-runtime'
import type { ChartOption } from './echarts-runtime'
import './chart-host.css'

type ChartHostProps = {
  name: string
  option: ChartOption
  connect?: (chart: EChartsType, reportFailure: () => void) => ChartConnection
}

export type ChartConnection = { setOption: (option: ChartOption) => void; dispose: () => void }

type LegendSelection = Record<string, boolean>
type SeriesSelection = SelectChangedEvent['selected']

export function ChartHost({ name, option, connect }: ChartHostProps) {
  const { theme } = useDidrahTheme()
  const container = useRef<HTMLDivElement>(null)
  const latestOption = useRef(option)
  const syncChart = useRef<(() => void) | null>(null)
  const legendSelection = useRef<LegendSelection>({})
  const seriesSelection = useRef<SeriesSelection>([])
  const [unavailable, setUnavailable] = useState(false)

  useLayoutEffect(() => {
    latestOption.current = option
  }, [option])

  useEffect(() => {
    const element = container.current
    if (!element) return

    let active = true
    let fontsReady = false
    let instance: EChartsType | undefined
    let connection: ChartConnection | undefined
    let renderedOption: ChartOption | undefined
    let failedOption: ChartOption | undefined
    let width = 0
    let height = 0

    function disposeChart() {
      if (!instance) return
      connection?.dispose()
      connection = undefined
      instance.off('legendselectchanged')
      instance.off('selectchanged')
      instance.dispose()
      instance = undefined
    }

    function showError() {
      disposeChart()
      if (active) setUnavailable(true)
    }

    function synchronize() {
      if (!active || !fontsReady || !element) return
      const nextWidth = element.clientWidth
      const nextHeight = element.clientHeight
      const nextOption = latestOption.current
      if (!nextWidth || !nextHeight || nextOption === failedOption) return

      try {
        if (!instance) {
          instance = init(element, chartThemes[theme].theme, {
            renderer: 'canvas',
            devicePixelRatio: Math.min(window.devicePixelRatio, 2),
            width: nextWidth,
            height: nextHeight,
          })
          width = nextWidth
          height = nextHeight
          renderedOption = undefined
          const connectedChart = instance
          connection = connect?.(connectedChart, () => {
            if (!active || instance !== connectedChart || !renderedOption) return
            failedOption = renderedOption
            showError()
          })
          if (!connection) {
            instance.on('legendselectchanged', (event) => {
              legendSelection.current = (event as { selected: LegendSelection }).selected
            })
            instance.on('selectchanged', (event) => {
              seriesSelection.current = (event as SelectChangedEvent).selected
            })
          }
        }

        if (renderedOption !== nextOption && connection) {
          connection.setOption(nextOption)
          renderedOption = nextOption
          setUnavailable(false)
        } else if (renderedOption !== nextOption) {
          if (renderedOption) {
            legendSelection.current = {}
            seriesSelection.current = []
          }
          const legend = nextOption.legend
          const withSelection = (item: LegendComponentOption) => ({
            ...item,
            selected: { ...item.selected, ...legendSelection.current },
          })
          instance.setOption({
            ...nextOption,
            legend: Array.isArray(legend) ? legend.map(withSelection) : legend && withSelection(legend),
          }, { notMerge: true })
          for (const selection of seriesSelection.current) {
            instance.dispatchAction({ ...selection, type: 'select' }, { silent: true })
          }
          renderedOption = nextOption
          setUnavailable(false)
        }

        if (width !== nextWidth || height !== nextHeight) {
          instance.resize({ width: nextWidth, height: nextHeight, silent: true })
          width = nextWidth
          height = nextHeight
        }
      } catch {
        failedOption = nextOption
        showError()
      }
    }

    const observer = new ResizeObserver(synchronize)
    observer.observe(element)
    syncChart.current = synchronize
    void Promise.all([
      document.fonts.load(chartCanvasFont, 'فروش خالص 123'),
      document.fonts.load(chartTooltipFont, 'مقدار ثبت نشده است 123'),
    ]).then(() => {
      fontsReady = true
      synchronize()
    }, () => {
      if (active) showError()
    })

    return () => {
      active = false
      syncChart.current = null
      observer.disconnect()
      disposeChart()
    }
  }, [connect, theme])

  useEffect(() => {
    syncChart.current?.()
  }, [option])

  return (
    <div className="didrah-chart">
      <div className="didrah-chart-canvas" ref={container} role="img" aria-label={name} aria-hidden={unavailable || undefined} />
      {unavailable && (
        <div className="didrah-chart-error">
          <PanelState kind="error" title="نمودار در دسترس نیست" description="داده‌های نمودار در جدول همراه دیده می‌شوند." />
        </div>
      )}
    </div>
  )
}

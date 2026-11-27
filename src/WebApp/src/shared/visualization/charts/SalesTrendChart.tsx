import type { TooltipComponentOption } from 'echarts/components'
import type { ReactNode } from 'react'
import { useMemo } from 'react'
import { useDidrahTheme } from '../../design-system/theme/DidrahThemeProvider'
import type { ThemeName } from '../../design-system/tokens/theme-contract'
import { ChartHost } from './ChartHost'
import { chartThemes } from './chart-theme'
import type { ChartOption } from './echarts-runtime'
import { createLuminousSalesTrendOption } from './luminous-sales-trend'
import type { TrendFrame, TrendValues } from './luminous-sales-trend'
import { trendAnomalyPoints, useSalesChartAnimation, useSalesChartMotion } from './SalesChartMotion'
import { axisRange, chartValue, missing, SalesChartPanel, SalesChartState, tooltipContent } from './SalesChartPresentation'
import type { SalesChartPresentation, SalesChartValueAxis, TrendObservation } from './SalesChartPresentation'

export type { TrendObservation } from './SalesChartPresentation'

export type SalesTrendChartProps = SalesChartPresentation & {
  /** Supply null while loading. Supply an empty array when there are no observations. */
  data: readonly TrendObservation[] | null
  currentLabel?: string
  previousLabel?: string
  note?: ReactNode
}

type TooltipFormatter = Exclude<NonNullable<TooltipComponentOption['formatter']>, string>
const emptyTrend: readonly TrendObservation[] = []

const trendTooltip = (observations: readonly TrendObservation[], unit: string): TooltipFormatter => (params) => {
  const points = Array.isArray(params) ? params : [params]
  const index = points[0]?.dataIndex
  const row = observations[index]
  if (!row) return ''

  const rows = points.filter((point) => point.componentType === 'series').map((point) => ({
    label: point.seriesName ?? '',
    value: point.seriesId === 'current' ? row.current : row.previous,
  }))
  return tooltipContent(`${row.day} · ${unit}`, rows)
}

function createTrendOption(
  name: ThemeName,
  sales: readonly TrendObservation[],
  values: TrendValues,
  trendRange: SalesChartValueAxis,
  currentName: string,
  previousName: string,
  unit: string,
): ChartOption {
  const theme = chartThemes[name]
  return {
    animation: false,
    grid: { top: 60, bottom: 38, left: 26, right: 42 },
    legend: {
      top: 14,
      right: 22,
      itemWidth: 18,
      itemHeight: 7,
      itemGap: 18,
      data: [previousName, currentName],
      align: 'right',
    },
    tooltip: { trigger: 'axis', renderMode: 'html', confine: true, formatter: trendTooltip(sales, unit) },
    xAxis: {
      type: 'category',
      inverse: true,
      boundaryGap: false,
      data: sales.map(({ day }) => day),
      axisLabel: { hideOverlap: true, margin: 12 },
    },
    yAxis: { type: 'value', position: 'right', ...trendRange },
    series: [
      {
        id: 'current',
        name: currentName,
        type: 'line',
        data: values.current,
        smooth: false,
        showSymbol: false,
        symbolSize: 8,
        lineStyle: { color: theme.primary, width: 3, shadowBlur: name === 'dark' ? 9 : 0, shadowColor: theme.highlightShadow },
        itemStyle: { color: theme.primary },
        emphasis: { focus: 'series', lineStyle: { width: 4 } },
        areaStyle: {
          color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [
            { offset: 0, color: theme.areaStart },
            { offset: 1, color: theme.areaEnd },
          ] },
        },
        markPoint: {
          silent: true,
          symbol: 'diamond',
          symbolSize: 13,
          label: { show: true, position: 'bottom', distance: 6, color: theme.anomaly, formatter: '{b}' },
          itemStyle: { color: theme.anomaly, borderWidth: 2, borderColor: theme.plot },
          data: trendAnomalyPoints(sales, values.current),
        },
      },
      {
        id: 'previous',
        name: previousName,
        type: 'line',
        data: values.previous,
        connectNulls: false,
        smooth: false,
        showSymbol: true,
        symbol: 'emptyCircle',
        symbolSize: 6,
        itemStyle: { color: theme.comparison },
        lineStyle: { color: theme.comparison, width: 2, type: 'dashed' },
        emphasis: { focus: 'series', lineStyle: { width: 3 } },
      },
    ],
  }
}

function SalesValues({ observations, currentName, previousName, unit }: {
  observations: readonly TrendObservation[]
  currentName: string
  previousName: string
  unit: string
}) {
  return (
    <details className="didrah-sales-chart-table">
      <summary>مقادیر نمودار روند فروش</summary>
      <table>
        <caption>فروش خالص روزانه به {unit}</caption>
        <thead><tr><th scope="col">روز</th><th scope="col">{currentName}</th><th scope="col">{previousName}</th></tr></thead>
        <tbody>
          {observations.map(({ id, day, current, previous, anomaly }) => (
            <tr key={id}>
              <th scope="row">{day}{anomaly && <small>{anomaly}</small>}</th>
              <td>{current === null ? missing : <bdi dir="ltr">{current}</bdi>}</td>
              <td>{previous === null ? missing : <bdi dir="ltr">{previous}</bdi>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  )
}

export function SalesTrendChart({
  data, title, description, unit, accessibleName = title, regionLabel, className,
  variant = 'default', animation, valueAxis, note,
  currentLabel = 'دورهٔ جاری', previousLabel = 'دورهٔ قبل',
}: SalesTrendChartProps) {
  const { theme } = useDidrahTheme()
  const observations = data ?? emptyTrend
  const luminous = variant === 'luminous' && theme === 'dark'
  const { enabled, frameRate, replay } = useSalesChartAnimation(luminous, animation)
  const mapped = useMemo(() => {
    const values = {
      current: observations.map(({ current }) => chartValue(current)),
      previous: observations.map(({ previous }) => chartValue(previous)),
    }
    const range = valueAxis ?? axisRange([...values.current, ...values.previous])
    const option = createTrendOption(theme, observations, values, range, currentLabel, previousLabel, unit)
    const frame: TrendFrame = { reveal: 1 }
    return {
      option: luminous ? createLuminousSalesTrendOption(option, frame) : option,
      trend: luminous ? { rows: observations, accepted: values, frame } : undefined,
      identity: JSON.stringify(observations.map(({ id, day, current, previous, anomaly }) => [id, day, current, previous, anomaly])),
      structure: JSON.stringify([range, unit, currentLabel, previousLabel, observations.map(({ id, day, anomaly }, index) =>
        [id, day, anomaly, values.current[index] === null, values.previous[index] === null],
      )]),
      hasValues: [...values.current, ...values.previous].some((value) => value !== null),
    }
  }, [observations, theme, luminous, valueAxis, currentLabel, previousLabel, unit])
  const request = useMemo(() => ({ ...mapped, replay, enabled, frameRate }), [mapped, replay, enabled, frameRate])
  const animated = useSalesChartMotion(request)
  const chart = variant === 'luminous' ? animated : { option: mapped.option }
  const chartNote = note ?? (observations.some(({ anomaly }) => anomaly)
    ? 'نشان لوزی، رویداد ثبت‌شده را نشان می‌دهد.'
    : null)

  return (
    <SalesChartPanel kind="trend" {...{ title, description, variant, className, regionLabel }}>
      {mapped.hasValues
        ? <ChartHost name={accessibleName} {...chart} />
        : <SalesChartState loading={data === null} loadingTitle="در حال دریافت داده‌های فروش" emptyTitle="داده‌ای برای روند فروش وجود ندارد" />}
      {data !== null && (
        <>
          {chartNote && <p className="didrah-sales-chart-note">{chartNote}</p>}
          <SalesValues observations={observations} currentName={currentLabel} previousName={previousLabel} unit={unit} />
        </>
      )}
    </SalesChartPanel>
  )
}

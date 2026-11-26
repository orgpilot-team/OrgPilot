import type { TooltipComponentOption } from 'echarts/components'
import type { ReactNode } from 'react'
import { useMemo } from 'react'
import { useDidrahTheme } from '../../design-system/theme/DidrahThemeProvider'
import type { ThemeName } from '../../design-system/tokens/theme-contract'
import { ChartHost } from './ChartHost'
import { chartThemes } from './chart-theme'
import type { ChartOption } from './echarts-runtime'
import { createLuminousBranchSalesOption } from './luminous-branch-sales'
import { useSalesChartAnimation, useSalesChartMotion } from './SalesChartMotion'
import { axisRange, chartValue, missing, SalesChartPanel, SalesChartState, tooltipContent } from './SalesChartPresentation'
import type { BranchObservation, SalesChartPresentation, SalesChartValueAxis } from './SalesChartPresentation'

export type { BranchObservation } from './SalesChartPresentation'

export type BranchSalesChartProps = SalesChartPresentation & {
  /** Supply null while loading. Supply an empty array when there are no observations. */
  data: readonly BranchObservation[] | null
  target: string | null
  seriesLabel?: string
  salesLabel?: string
  targetLabel?: string
  note?: ReactNode
}

type TooltipFormatter = Exclude<NonNullable<TooltipComponentOption['formatter']>, string>
const emptyBranches: readonly BranchObservation[] = []

const branchTooltip = (observations: readonly BranchObservation[], target: string | null, unit: string, salesLabel: string, targetLabel: string): TooltipFormatter => (params) => {
  const point = Array.isArray(params) ? params[0] : params
  const branch = observations[point?.dataIndex]
  if (!branch) return ''
  return tooltipContent(`شعبهٔ ${branch.name} · \u2066${branch.code}\u2069`, [
    { label: `${salesLabel} (${unit})`, value: branch.sales },
    { label: targetLabel, value: target },
  ])
}

function createBranchOption(
  name: ThemeName,
  branches: readonly BranchObservation[],
  branchValues: (number | null)[],
  branchRange: SalesChartValueAxis,
  target: string | null,
  targetValue: number | null,
  { unit, seriesLabel, salesLabel, targetLabel }: { unit: string; seriesLabel: string; salesLabel: string; targetLabel: string },
): ChartOption {
  const theme = chartThemes[name]
  return {
    animation: false,
    grid: { top: 40, bottom: 36, left: 24, right: 79 },
    tooltip: { trigger: 'item', renderMode: 'html', confine: true, formatter: branchTooltip(branches, target, unit, salesLabel, targetLabel) },
    xAxis: { type: 'value', inverse: true, ...branchRange, axisLabel: { hideOverlap: true } },
    yAxis: { type: 'category', position: 'right', inverse: true, data: branches.map(({ name }) => name) },
    series: [{
      id: 'branch-sales',
      type: 'bar',
      name: seriesLabel,
      data: branches.map((branch, index) => ({
        id: branch.code,
        // ECharts uses the item name as the selection key. The axis and tooltip use the display name.
        name: branch.code,
        value: branchValues[index],
      })),
      barMaxWidth: 18,
      selectedMode: 'single',
      itemStyle: { color: theme.primary, borderRadius: [5, 0, 0, 5] },
      emphasis: { itemStyle: { color: theme.comparison } },
      select: { itemStyle: { color: theme.comparison, borderColor: theme.focus, borderWidth: 2 } },
      markLine: {
        silent: true,
        symbol: ['none', 'none'],
        label: { show: true, position: 'start', rotate: 0, distance: 8, color: theme.target, formatter: `${targetLabel} \u2066${target}\u2069` },
        lineStyle: { color: theme.target, width: 1.5, type: 'dashed' },
        data: targetValue === null ? [] : [{ xAxis: targetValue }],
      },
    }],
  }
}

function BranchValues({ observations, goal, unit, salesLabel, targetLabel }: {
  observations: readonly BranchObservation[]
  goal: string | null
  unit: string
  salesLabel: string
  targetLabel: string
}) {
  return (
    <details className="didrah-sales-chart-table">
      <summary>مقادیر نمودار فروش شعب</summary>
      <table>
        <caption>فروش خالص و {targetLabel} به {unit}</caption>
        <thead><tr><th scope="col">شعبه</th><th scope="col">{salesLabel}</th><th scope="col">{targetLabel}</th></tr></thead>
        <tbody>
          {observations.map((branch) => (
            <tr key={branch.code}>
              <th scope="row">{branch.name}<small><bdi dir="ltr" lang="en">{branch.code}</bdi></small></th>
              <td>{branch.sales === null ? missing : <bdi dir="ltr">{branch.sales}</bdi>}</td>
              <td>{goal === null ? missing : <bdi dir="ltr">{goal}</bdi>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  )
}

export function BranchSalesChart({
  data, target, title, description, unit, accessibleName = title, regionLabel, className,
  variant = 'default', animation, valueAxis, seriesLabel = 'فروش شعبه', salesLabel, targetLabel = 'هدف', note,
}: BranchSalesChartProps) {
  const { theme } = useDidrahTheme()
  const observations = data ?? emptyBranches
  const luminous = variant === 'luminous' && theme === 'dark'
  const { enabled, frameRate, replay } = useSalesChartAnimation(luminous, animation)
  const mapped = useMemo(() => {
    const values = observations.map(({ sales }) => chartValue(sales))
    const targetValue = chartValue(target)
    const range = valueAxis ?? axisRange([...values, targetValue])
    const option = createBranchOption(theme, observations, values, range, target, targetValue, {
      unit, seriesLabel, salesLabel: salesLabel ?? 'فروش خالص', targetLabel,
    })
    return {
      option: luminous ? createLuminousBranchSalesOption(option) : option,
      identity: JSON.stringify([observations.map(({ code, name, sales }) => [code, name, sales]), target]),
      structure: JSON.stringify([
        range, unit, seriesLabel, salesLabel, targetLabel, target,
        observations.map(({ code, name }, index) => [code, name, values[index] === null]),
      ]),
      hasValues: values.some((value) => value !== null),
    }
  }, [observations, target, theme, luminous, valueAxis, unit, seriesLabel, salesLabel, targetLabel])
  const request = useMemo(() => ({ ...mapped, replay, enabled, frameRate }), [mapped, replay, enabled, frameRate])
  const animated = useSalesChartMotion(request)
  const chart = variant === 'luminous' ? animated : { option: mapped.option }
  const chartNote = note ?? (target === null ? null :
    <>خط‌چین، {targetLabel} <bdi dir="ltr">{target}</bdi> ({unit}) را نشان می‌دهد.</>)

  return (
    <SalesChartPanel kind="branch" {...{ title, description, variant, className, regionLabel }}>
      {mapped.hasValues
        ? <ChartHost name={accessibleName} {...chart} />
        : <SalesChartState loading={data === null} loadingTitle="در حال دریافت داده‌های شعب" emptyTitle="داده‌ای برای فروش شعب وجود ندارد" />}
      {data !== null && (
        <>
          {chartNote && <p className="didrah-sales-chart-note">{chartNote}</p>}
          <BranchValues observations={observations} goal={target} unit={unit} salesLabel={salesLabel ?? 'فروش'} targetLabel={targetLabel} />
        </>
      )}
    </SalesChartPanel>
  )
}

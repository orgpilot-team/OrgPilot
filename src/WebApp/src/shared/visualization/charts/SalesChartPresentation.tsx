import type { PropsWithChildren, ReactNode } from 'react'
import { Panel, SectionHeader } from '../../design-system/patterns/Panel'
import { PanelState } from '../../design-system/patterns/PanelState'
import type { ChartFrameRate } from './chart-motion'
import './sales-chart.css'
import './luminous-chart.css'

/** Supply ordered observations with stable IDs. Decimal strings retain the supplied display precision. */
export type TrendObservation = {
  id: string
  day: string
  current: string | null
  previous: string | null
  anomaly?: string
}

/** Supply ordered observations with stable branch codes and decimal strings. Null marks a missing sale. */
export type BranchObservation = { name: string; code: string; sales: string | null }

export type SalesChartAnimation = {
  enabled?: boolean
  frameRate?: ChartFrameRate
  /** Change this key to replay the entrance with the current data. */
  replayKey?: number
}

export type SalesChartValueAxis = { min: number; max: number; interval: number }

export type SalesChartPresentation = {
  title: string
  description?: ReactNode
  unit: string
  accessibleName?: string
  regionLabel?: string
  className?: string
  variant?: 'default' | 'luminous'
  /** Dark Mode luminous motion. The default variant and Light Mode are static. */
  animation?: SalesChartAnimation
  /** Set an explicit value axis instead of fitting the observations. */
  valueAxis?: SalesChartValueAxis
}

export const missing = 'ثبت نشده'

export function chartValue(value: string | null) {
  if (value === null || value.trim() === '') return null
  const numeric = Number(value)
  return Number.isFinite(numeric) ? numeric : null
}

export function axisRange(values: (number | null)[]): SalesChartValueAxis {
  let low = 0
  let high = 0
  for (const value of values) {
    if (value === null) continue
    low = Math.min(low, value)
    high = Math.max(high, value)
  }
  const gap = (high - low) / 4 || .25
  const base = 10 ** Math.floor(Math.log10(gap))
  const unit = [1, 2, 2.5, 5, 10].find((step) => step >= gap / base) ?? 10
  const interval = unit * base
  return {
    min: Math.floor(low / interval) * interval || 0,
    max: Math.ceil(high / interval) * interval || (low === 0 ? interval * 4 : 0),
    interval,
  }
}

type TooltipRow = { label: string; value: string | null }

export function tooltipContent(title: string, rows: TooltipRow[]) {
  const content = document.createElement('div')
  content.className = 'didrah-sales-chart-tooltip'
  content.dir = 'rtl'
  const heading = document.createElement('strong')
  heading.textContent = title
  content.append(heading)

  for (const { label, value } of rows) {
    const row = document.createElement('div')
    const name = document.createElement('span')
    const amount = document.createElement('bdi')
    name.textContent = label
    amount.dir = value === null ? 'rtl' : 'ltr'
    amount.textContent = value ?? missing
    row.append(name, amount)
    content.append(row)
  }
  return content
}

type SalesChartPanelProps = PropsWithChildren<
  Pick<SalesChartPresentation, 'title' | 'description' | 'className' | 'regionLabel' | 'variant'>
  & { kind: 'trend' | 'branch' }
>

export function SalesChartPanel({ title, description, variant, className, regionLabel, kind, children }: SalesChartPanelProps) {
  const luminousClass = variant === 'luminous' ? `didrah-luminous-chart didrah-luminous-chart--${kind}` : undefined
  const classes = [className, luminousClass].filter(Boolean).join(' ')
  const panel = (
    <Panel surface="raised" density="compact">
      <SectionHeader title={title} description={description} />
      {children}
    </Panel>
  )
  return classes || regionLabel ? <section className={classes || undefined} aria-label={regionLabel}>{panel}</section> : panel
}

export function SalesChartState({ loading, loadingTitle, emptyTitle }: { loading: boolean; loadingTitle: string; emptyTitle: string }) {
  return loading ? <PanelState kind="loading" title={loadingTitle} /> : <PanelState kind="empty" title={emptyTitle} />
}

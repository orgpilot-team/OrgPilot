import type { BarSeriesOption } from 'echarts/charts'
import { luminousChartAxisLabel } from './chart-theme'
import type { ChartOption } from './echarts-runtime'

const blueFill = {
  type: 'linear',
  x: 0,
  y: 0,
  x2: 0,
  y2: 1,
  colorStops: [
    { offset: 0, color: '#a5dcff' },
    { offset: .12, color: '#63b6ff' },
    { offset: .30, color: '#2785ff' },
    { offset: .61, color: '#1259f4' },
    { offset: 1, color: '#1239bb' },
  ],
} satisfies NonNullable<BarSeriesOption['itemStyle']>['color']

export function createLuminousBranchSalesOption(original: ChartOption): ChartOption {
  const bar = Array.isArray(original.series) ? original.series[0] : original.series
  const xAxis = Array.isArray(original.xAxis) ? original.xAxis[0] : original.xAxis
  const yAxis = Array.isArray(original.yAxis) ? original.yAxis[0] : original.yAxis
  if (bar?.type !== 'bar' || xAxis?.type !== 'value' || yAxis?.type !== 'category') return original

  const styledBar: BarSeriesOption = {
    ...bar,
    data: bar.data?.map((item) => (
      item && typeof item === 'object' && 'value' in item && typeof item.value === 'number' && item.value < 0
        ? { ...item, itemStyle: { ...item.itemStyle, borderRadius: [0, 6, 6, 0] } }
        : item
    )),
    barMaxWidth: 22,
    itemStyle: {
      ...bar.itemStyle,
      color: blueFill,
      borderRadius: [6, 0, 0, 6],
      borderColor: '#a9caff48',
      borderWidth: .75,
      shadowColor: '#1269ff8c',
      shadowBlur: 11,
    },
    markLine: {
      ...bar.markLine,
      label: {
        ...bar.markLine?.label,
        color: '#c3eaff',
        backgroundColor: '#101c39',
        borderColor: '#72bbf450',
        borderWidth: 1,
        borderRadius: 5,
        padding: [3, 6],
      },
      lineStyle: {
        color: '#a3ddffe0',
        width: 1.25,
        type: [4, 4],
        shadowColor: '#46b7fa80',
        shadowBlur: 5,
      },
    },
  }

  return {
    ...original,
    backgroundColor: 'transparent',
    grid: { top: 42, bottom: 34, left: 20, right: 71 },
    xAxis: {
      ...xAxis,
      axisLabel: { ...xAxis.axisLabel, color: '#adbce1', margin: 11 },
      splitLine: { lineStyle: { color: '#577bb34b', type: [3, 3], width: 1 } },
    },
    yAxis: {
      ...yAxis,
      axisLabel: { ...yAxis.axisLabel, color: luminousChartAxisLabel, margin: 10 },
      axisLine: { show: true, lineStyle: { color: '#6484b56b' } },
    },
    series: [styledBar],
  }
}

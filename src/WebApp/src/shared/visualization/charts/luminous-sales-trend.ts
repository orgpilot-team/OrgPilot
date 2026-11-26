import { CustomChart } from 'echarts/charts'
import type { CustomSeriesOption, LineSeriesOption } from 'echarts/charts'
import { use } from 'echarts/core'
import { luminousChartAxisLabel } from './chart-theme'
import type { ChartOption } from './echarts-runtime'

use([CustomChart])

type Stops = ReadonlyArray<readonly [number, string]>
type Plot = { x: number; y: number; width: number; height: number }
type Point = { x: number; y: number }
type RenderItem = NonNullable<CustomSeriesOption['renderItem']>
export type TrendValues = { current: (number | null)[]; previous: (number | null)[] }
export type TrendFrame = { reveal: number; values?: TrendValues }

// Scale the approved NeuroAI stroke and blur dimensions to the live plot width.
const referencePlotWidth = 1376
const blue = {
  area: [
    [0, '#2079ffe8'], [.16, '#1455ffde'], [.37, '#005aec6e'], [.74, '#003a9e29'], [1, '#04245d14'],
  ] satisfies Stops,
  stroke: [
    [0, '#0452dc'], [.12, '#075ef6'], [.21, '#128dff'], [.28, '#037cf4'], [.36, '#0483ff'],
    [.41, '#337fff'], [.47, '#2785ff'], [.53, '#1771fa'], [.65, '#2b7dff'], [.78, '#3578ff'],
    [.84, '#56a1ff'], [.90, '#459aff'], [.96, '#0769f9'], [1, '#0649d2'],
  ] satisfies Stops,
  halo: [
    { color: '#1648ff', width: 18, blur: 7.3, opacity: .64 },
    { color: '#006bff', width: 10, blur: 3.2, opacity: .65 },
  ],
}
const cyan = {
  area: [
    [0, '#0ee9ff3d'], [.32, '#05c8dd30'], [.62, '#03c3da30'], [.81, '#007ba730'], [1, '#002b4908'],
  ] satisfies Stops,
  stroke: [
    [0, '#075268'], [.05, '#0bcbd9'], [.17, '#00ecff'], [.38, '#00f5fb'], [.68, '#00f1f6'],
    [.83, '#0deafa'], [.93, '#02effb'], [.95, '#08dadc'], [.98, '#008697'], [1, '#07566d'],
  ] satisfies Stops,
  halo: [
    { color: '#00dbe9', width: 16, blur: 7.3, opacity: .51 },
    { color: '#08d7fa', width: 8, blur: 3.2, opacity: .25 },
  ],
}
const cyanAreaFade: Stops = [[.86, '#fff'], [.95, '#fffc'], [1, '#ffffff42']]
const cyanHaloFade: Stops = [
  [0, '#fff0'], [.14, '#ffffff52'], [.65, '#ffffff42'], [.81, '#fff9'], [.91, '#fff'], [1, '#ffffff1f'],
]
const highlight: Stops = [
  [0, '#b6e7ffe6'], [.22, '#9cd6ffe6'], [.42, '#3eb8ff21'], [.83, '#59c6ff57'], [1, '#00b6ff05'],
]
const gridFade: Stops = [[0, '#ffffffb0'], [.22, '#fff'], [.83, '#fffc'], [1, '#ffffff75']]

function layer(plot: Plot, dpr: number, z2: number, image = document.createElement('canvas')) {
  const { x, y, width, height } = plot
  const pixelWidth = Math.ceil(width * dpr)
  const pixelHeight = Math.ceil(height * dpr)
  if (image.width !== pixelWidth) image.width = pixelWidth
  if (image.height !== pixelHeight) image.height = pixelHeight
  const context = image.getContext('2d')
  if (!context) return
  context.setTransform(pixelWidth / width, 0, 0, pixelHeight / height, 0, 0)
  context.clearRect(0, 0, width, height)
  return { context, element: { type: 'image' as const, z2, style: { image, x, y, width, height } } }
}

function addStops(gradient: CanvasGradient, stops: Stops) {
  for (const [offset, color] of stops) gradient.addColorStop(offset, color)
  return gradient
}

function fadeHorizontally(context: CanvasRenderingContext2D, plot: Plot, stops: Stops) {
  context.save()
  context.globalCompositeOperation = 'destination-in'
  context.fillStyle = addStops(context.createLinearGradient(0, 0, plot.width, 0), stops)
  context.fillRect(0, 0, plot.width, plot.height)
  context.restore()
}

function plotBounds(system: Parameters<RenderItem>[0]['coordSys']): Plot | undefined {
  if (system.type !== 'cartesian2d') return
  const plot = system as typeof system & Plot
  if (plot.width > 0 && plot.height > 0) return plot
}

function drawGrid(categoryCount: number, min: number, max: number, interval: number): RenderItem {
  let cached: ReturnType<typeof layer>
  let lastLayout = ''
  return ({ coordSys }, api) => {
    const plot = plotBounds(coordSys)
    if (!plot) return
    const dpr = api.getDevicePixelRatio()
    const layout = JSON.stringify([plot.x, plot.y, plot.width, plot.height, dpr])
    if (layout === lastLayout) return cached?.element
    const grid = layer(plot, dpr, 3, cached?.element.style.image)
    if (!grid) return
    cached = grid
    lastLayout = layout

    const { context } = grid
    const { width, height, x, y } = plot
    const scale = Math.max(.4, width / referencePlotWidth)
    context.strokeStyle = '#456ab8'
    context.lineWidth = Math.max(.75, 1.45 * scale)
    context.setLineDash([7 * scale, 4.3 * scale])
    const tickCount = Math.round((max - min) / interval)
    for (let index = 0; index <= tickCount; index++) {
      const tick = min + index * interval
      const ordinate = api.coord([0, tick])[1] - y
      context.globalAlpha = index === tickCount ? .31 : .49
      context.beginPath()
      context.moveTo(0, ordinate)
      context.lineTo(width, ordinate)
      context.stroke()
    }
    context.globalAlpha = .45
    context.setLineDash([6 * scale, 4.3 * scale])
    context.beginPath()
    for (let index = 1; index < categoryCount - 1; index++) {
      const abscissa = api.coord([index, 0])[0] - x
      context.moveTo(abscissa, 0)
      context.lineTo(abscissa, height)
    }
    context.stroke()
    context.setLineDash([])
    context.globalAlpha = .44
    context.beginPath()
    context.moveTo(width - .5, 0)
    context.lineTo(width - .5, height)
    context.stroke()
    context.globalAlpha = 1
    fadeHorizontally(context, plot, gridFade)
    return grid.element
  }
}

function tangent(points: Point[], index: number) {
  const point = points[index]
  const before = points[index - 1]
  const after = points[index + 1]
  if (!before) return after ? after.y - point.y : 0
  if (!after) return point.y - before.y
  const incoming = point.y - before.y
  const outgoing = after.y - point.y
  if (Math.sign(incoming) !== Math.sign(outgoing)) return 0
  return Math.sign(incoming) * Math.min(Math.abs(incoming), Math.abs(outgoing))
}

function fadeGapEdges(context: CanvasRenderingContext2D, plot: Plot, segments: Point[][]) {
  if (segments.length < 2) return
  context.save()
  context.globalCompositeOperation = 'destination-out'
  for (const points of segments) {
    const first = points[0].x
    const last = points[points.length - 1].x
    const left = Math.min(first, last)
    const right = Math.max(first, last)
    const fade = Math.min(12, (right - left) / 2)
    if (!fade) continue
    for (const edge of [left, right]) {
      if (edge < .5 || edge > plot.width - .5) continue
      const inside = edge === left ? edge + fade : edge - fade
      context.fillStyle = addStops(context.createLinearGradient(edge, 0, inside, 0), [[0, '#fff'], [1, '#fff0']])
      context.fillRect(Math.min(edge, inside), 0, fade, plot.height)
    }
  }
  context.restore()
}

function drawSeries(data: LineSeriesOption['data'], isCurrent: boolean, inverse: boolean, frame?: TrendFrame): RenderItem {
  let cached: { area: NonNullable<ReturnType<typeof layer>>; stroke: NonNullable<ReturnType<typeof layer>> } | undefined
  let lastLayout = ''
  let lastValues: typeof data
  return ({ coordSys }, api) => {
    const plot = plotBounds(coordSys)
    if (!plot) return
    const { x, y, width, height } = plot
    const dpr = api.getDevicePixelRatio()
    const values = frame?.values?.[isCurrent ? 'current' : 'previous'] ?? data
    const reveal = frame?.reveal ?? 1
    const visibleWidth = width * reveal
    const clipPath = reveal < 1 ? {
      type: 'rect' as const,
      shape: { x: inverse ? x + width - visibleWidth : x, y, width: visibleWidth, height },
    } : false
    const layout = JSON.stringify([x, y, width, height, dpr])
    if (cached && layout === lastLayout && values === lastValues) {
      return { type: 'group', clipPath, children: [cached.area.element, cached.stroke.element] }
    }
    const area = layer(plot, dpr, isCurrent ? 0 : 1, cached?.area.element.style.image)
    const stroke = layer(plot, dpr, isCurrent ? 5 : 4, cached?.stroke.element.style.image)
    if (!area || !stroke) return
    cached = { area, stroke }
    lastLayout = layout
    lastValues = values

    const baseline = api.coord([0, 0])[1] - y
    const linePath = new Path2D()
    const areaPath = new Path2D()
    const segments: Point[][] = []
    let segment: Point[] = []
    let top = baseline
    let bottom = baseline

    values?.forEach((value, index) => {
      if (typeof value !== 'number' || !Number.isFinite(value)) {
        segment = []
        return
      }
      const point = api.coord([index, value])
      if (segment.length === 0) segments.push(segment)
      segment.push({ x: point[0] - x, y: point[1] - y })
      top = Math.min(top, point[1] - y)
      bottom = Math.max(bottom, point[1] - y)
    })

    for (const points of segments) {
      const first = points[0]
      const last = points[points.length - 1]
      const curve = new Path2D()
      curve.moveTo(first.x, first.y)
      for (let index = 1; index < points.length; index++) {
        const before = points[index - 1]
        const after = points[index]
        const handle = (after.x - before.x) / 3
        // Keep both control points between the observations to prevent overshoot.
        curve.bezierCurveTo(
          before.x + handle, before.y + tangent(points, index - 1) / 3,
          after.x - handle, after.y - tangent(points, index) / 3,
          after.x, after.y,
        )
      }
      linePath.addPath(curve)
      curve.lineTo(last.x, baseline)
      curve.lineTo(first.x, baseline)
      curve.closePath()
      areaPath.addPath(curve)
    }

    const palette = isCurrent ? blue : cyan
    if (top < baseline) {
      const crossesZero = bottom > baseline
      if (crossesZero) {
        area.context.save()
        area.context.beginPath()
        area.context.rect(0, 0, width, baseline)
        area.context.clip()
      }
      area.context.fillStyle = addStops(area.context.createLinearGradient(0, top, 0, baseline), palette.area)
      area.context.fill(areaPath)
      if (crossesZero) area.context.restore()
    }
    if (bottom > baseline) {
      area.context.save()
      area.context.beginPath()
      area.context.rect(0, baseline, width, height - baseline)
      area.context.clip()
      area.context.fillStyle = addStops(area.context.createLinearGradient(0, bottom, 0, baseline), palette.area)
      area.context.fill(areaPath)
      area.context.restore()
    }
    if (!isCurrent) {
      fadeHorizontally(area.context, plot, cyanAreaFade)
      fadeGapEdges(area.context, plot, segments)
    }

    const scale = Math.max(.4, width / referencePlotWidth)
    const { context } = stroke
    context.lineCap = 'round'
    context.lineJoin = 'round'
    for (const { color, width: haloWidth, blur, opacity } of palette.halo) {
      context.globalAlpha = opacity
      context.filter = `blur(${blur * scale * dpr}px)`
      context.strokeStyle = color
      context.lineWidth = haloWidth * scale
      context.stroke(linePath)
    }
    context.filter = 'none'
    context.globalAlpha = 1
    if (!isCurrent) fadeHorizontally(context, plot, cyanHaloFade)
    context.strokeStyle = addStops(context.createLinearGradient(0, 0, width, 0), palette.stroke)
    context.lineWidth = 5.6 * scale
    context.stroke(linePath)

    if (isCurrent) {
      context.fillStyle = '#56a1ff'
      for (const points of segments) {
        if (points.length !== 1) continue
        context.beginPath()
        context.arc(points[0].x, points[0].y, 2.8 * scale, 0, Math.PI * 2)
        context.fill()
      }
      context.translate(0, -.45 * scale)
      context.lineWidth = 2.4 * scale
      context.strokeStyle = addStops(context.createLinearGradient(0, top, 0, height - 8 * scale), highlight)
      context.stroke(linePath)
    }

    return { type: 'group', clipPath, children: [area.element, stroke.element] }
  }
}

function visualLayer(id: string, name: string, renderItem: RenderItem): CustomSeriesOption {
  return {
    type: 'custom',
    id,
    name,
    z: 1,
    silent: true,
    tooltip: { show: false, trigger: 'none' },
    // One render call for the whole layer. The native series supplies axis and tooltip values.
    data: [0],
    encode: { x: -1, y: -1, tooltip: [] },
    renderItem,
  }
}

export function createLuminousSalesTrendOption(trend: ChartOption, frame?: TrendFrame): ChartOption {
  const xAxis = Array.isArray(trend.xAxis) ? trend.xAxis[0] : trend.xAxis
  const yAxis = Array.isArray(trend.yAxis) ? trend.yAxis[0] : trend.yAxis
  const legend = Array.isArray(trend.legend) ? trend.legend[0] : trend.legend
  if (xAxis?.type !== 'category' || yAxis?.type !== 'value') return trend
  const { min, max, interval } = yAxis
  if (typeof min !== 'number' || typeof max !== 'number' || typeof interval !== 'number' || !(interval > 0)) return trend
  const series = Array.isArray(trend.series) ? trend.series : [trend.series]
  const lines = series.filter((item): item is LineSeriesOption => item?.type === 'line')

  const interactiveLines = lines.map((line): LineSeriesOption => ({
    ...line,
    lineStyle: { opacity: 0 },
    areaStyle: undefined,
    itemStyle: { color: line.id === 'current' ? '#005afe' : '#02fbff' },
    emphasis: { lineStyle: { opacity: 0 } },
    symbolSize: line.id === 'current' ? line.symbolSize : 5,
  }))
  const visualLines = lines.map((line) => (
    visualLayer(`${line.id}-lighting`, String(line.name), drawSeries(line.data, line.id === 'current', xAxis.inverse === true, frame))
  ))

  return {
    ...trend,
    backgroundColor: 'transparent',
    grid: { top: 14, bottom: 64, left: 25, right: 40 },
    xAxis: { ...xAxis, axisLabel: { ...xAxis.axisLabel, color: luminousChartAxisLabel }, axisLine: { show: false } },
    yAxis: { ...yAxis, axisLabel: { ...yAxis.axisLabel, color: luminousChartAxisLabel }, splitLine: { show: false } },
    legend: {
      ...legend,
      top: undefined,
      bottom: 8,
      right: 30,
      icon: 'circle',
      itemWidth: 10,
      itemHeight: 10,
      textStyle: { color: '#f4f5ff' },
    },
    series: [
      ...interactiveLines,
      ...visualLines,
      visualLayer('trend-grid', '', drawGrid(xAxis.data?.length ?? 0, min, max, interval)),
    ],
  }
}

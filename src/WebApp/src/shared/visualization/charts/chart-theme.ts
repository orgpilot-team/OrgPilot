import { darkTheme } from '../../design-system/tokens/dark-theme'
import { lightTheme } from '../../design-system/tokens/light-theme'
import { overlayShadow } from '../../design-system/tokens/layout'
import type { ThemeColors, ThemeName } from '../../design-system/tokens/theme-contract'
import { typography } from '../../design-system/tokens/typography'

const { roles } = typography
const captionSize = Number.parseFloat(roles.caption.size) * 16

export const chartCanvasFont = `${roles.caption.weight} ${captionSize}px ${typography.family}`
export const chartTooltipFont = `${roles.secondary.weight} ${roles.secondary.size} ${typography.family}`
export const luminousChartAxisLabel = '#d3dbfa'

function createChartTheme(name: ThemeName, colors: ThemeColors) {
  const dark = name === 'dark'
  const primary = colors[dark ? 'brand-indigo' : 'brand-primary']
  const comparison = colors['accent-cyan-content']
  const labels = { color: colors['text-secondary'], fontSize: captionSize }
  const axisLine = { show: true, lineStyle: { color: colors['border-control'] } }

  return {
    theme: {
      backgroundColor: colors['surface-input'],
      color: [primary, comparison],
      textStyle: { fontFamily: typography.family, fontSize: captionSize },
      categoryAxis: { axisLabel: labels, axisLine, axisTick: { show: false } },
      valueAxis: {
        axisLabel: labels,
        axisLine: { ...axisLine, show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: colors['border-subtle'] } },
      },
      legend: {
        textStyle: labels,
        inactiveColor: colors['text-muted'],
        inactiveBorderColor: colors['text-muted'],
      },
      tooltip: {
        renderMode: 'richText',
        backgroundColor: colors['surface-overlay'],
        borderColor: colors['border-control'],
        textStyle: {
          fontFamily: typography.family,
          fontSize: Number.parseFloat(roles.secondary.size) * 16,
          color: colors['text-primary'],
        },
        extraCssText: `box-shadow: ${overlayShadow(name, colors)}`,
        axisPointer: { lineStyle: { color: colors['border-control'] } },
      },
    },
    primary,
    comparison,
    target: colors['text-secondary'],
    anomaly: colors['status-critical'],
    focus: colors['focus-ring'],
    plot: colors['surface-input'],
    areaStart: `${primary}${dark ? '60' : '29'}`,
    areaEnd: `${primary}00`,
    highlightShadow: dark ? `${primary}80` : 'transparent',
  }
}

export const chartThemes = {
  dark: createChartTheme('dark', darkTheme),
  light: createChartTheme('light', lightTheme),
}

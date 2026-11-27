import type { ThemeColors, ThemeName } from './theme-contract'

export const layout = {
  space: { compact: 8, gap: 12, inset: 16, panel: 24 },
  radius: { control: 8, panel: 16 },
  controlHeight: 38,
} as const

export function overlayShadow(theme: ThemeName, colors: ThemeColors) {
  const shadow = theme === 'dark' ? `${colors.canvas}b3` : `${colors['text-primary']}1a`
  return `0 12px 32px ${shadow}, 0 0 0 1px ${colors['border-subtle']}`
}

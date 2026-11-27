import { primitiveColors as color } from './primitives'
import type { ThemeColors } from './theme-contract'

export const lightTheme = {
  canvas: color.porcelain,
  'surface-base': color.white,
  'surface-raised': color.ice,
  'surface-overlay': color.white,
  'surface-selected': color.lavender,
  'surface-input': color.pearl,
  'border-subtle': color.cloud,
  'border-control': color.steel,
  'focus-ring': color.electricBlue,
  'brand-primary': color.electricBlue,
  'brand-on-primary': color.white,
  'brand-indigo': color.indigo,
  'brand-cyan': color.brightCyan,
  'accent-cyan-content': color.deepCyan,
  'text-primary': color.deepNavy,
  'text-secondary': color.lead,
  'text-muted': color.stone,
  'status-success': color.emerald,
  'status-warning': color.ochre,
  'status-critical': color.crimson,
  'status-information': color.cobalt,
} satisfies ThemeColors

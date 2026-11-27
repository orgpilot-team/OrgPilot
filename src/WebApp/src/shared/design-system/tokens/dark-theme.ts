import { primitiveColors as color } from './primitives'
import type { ThemeColors } from './theme-contract'

export const darkTheme = {
  canvas: color.midnight,
  'surface-base': color.obsidian,
  'surface-raised': color.graphite,
  'surface-overlay': color.slate,
  'surface-selected': color.dusk,
  'surface-input': color.ink,
  'border-subtle': color.charcoal,
  'border-control': color.ash,
  'focus-ring': color.brightCyan,
  'brand-primary': color.electricBlue,
  'brand-on-primary': color.white,
  'brand-indigo': color.indigo,
  'brand-cyan': color.brightCyan,
  'accent-cyan-content': color.brightCyan,
  'text-primary': color.frost,
  'text-secondary': color.silver,
  'text-muted': color.mist,
  'status-success': color.mint,
  'status-warning': color.amber,
  'status-critical': color.coral,
  'status-information': color.sky,
} satisfies ThemeColors

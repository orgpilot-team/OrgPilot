export type ThemeName = 'dark' | 'light'
export type HexColor = `#${string}`

export type ColorRole =
  | 'canvas'
  | 'surface-base'
  | 'surface-raised'
  | 'surface-overlay'
  | 'surface-selected'
  | 'surface-input'
  | 'border-subtle'
  | 'border-control'
  | 'focus-ring'
  | 'brand-primary'
  | 'brand-on-primary'
  | 'brand-indigo'
  | 'brand-cyan'
  | 'accent-cyan-content'
  | 'text-primary'
  | 'text-secondary'
  | 'text-muted'
  | 'status-success'
  | 'status-warning'
  | 'status-critical'
  | 'status-information'

export type ThemeColors = Readonly<Record<ColorRole, HexColor>>

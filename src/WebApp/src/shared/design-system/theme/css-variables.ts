import type { ColorRole, ThemeColors, ThemeName } from '../tokens/theme-contract'
import { layout, overlayShadow } from '../tokens/layout'
import { fontWeights, typography } from '../tokens/typography'

export function colorVariableName(role: ColorRole) {
  return `--didrah-color-${role}` as const
}

export function applyThemeVariables(style: CSSStyleDeclaration, theme: ThemeName, colors: ThemeColors) {
  const roles = Object.keys(colors) as ColorRole[]

  for (const role of roles) {
    style.setProperty(colorVariableName(role), colors[role])
  }
  style.setProperty('--didrah-shadow-overlay', overlayShadow(theme, colors))

  return () => {
    for (const role of roles) {
      style.removeProperty(colorVariableName(role))
    }
    style.removeProperty('--didrah-shadow-overlay')
  }
}

export function applyLayout(style: CSSStyleDeclaration) {
  const properties = [
    ...Object.entries(layout.space).map(([key, value]) => [`--didrah-space-${key}`, value] as const),
    ...Object.entries(layout.radius).map(([key, value]) => [`--didrah-radius-${key}`, value] as const),
  ]

  for (const [name, value] of properties) {
    style.setProperty(name, `${value / 16}rem`)
  }

  return () => {
    for (const [name] of properties) {
      style.removeProperty(name)
    }
  }
}

export function applyTypography(style: CSSStyleDeclaration) {
  const properties = Object.entries(typography.roles)
  const weights = Object.entries(fontWeights)

  style.setProperty('--didrah-font-family', typography.family)
  for (const [name, weight] of weights) {
    style.setProperty(`--didrah-weight-${name}`, String(weight))
  }

  for (const [role, text] of properties) {
    style.setProperty(
      `--didrah-type-${role}`,
      `${text.weight} ${text.size}/${text.lineHeight} var(--didrah-font-family)`,
    )
  }

  return () => {
    style.removeProperty('--didrah-font-family')
    for (const [name] of weights) {
      style.removeProperty(`--didrah-weight-${name}`)
    }

    for (const [role] of properties) {
      style.removeProperty(`--didrah-type-${role}`)
    }
  }
}

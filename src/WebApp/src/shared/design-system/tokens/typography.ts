export const fontWeights = {
  regular: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
} as const

type TextStyle = {
  size: `${number}rem`
  weight: (typeof fontWeights)[keyof typeof fontWeights]
  lineHeight: number
}

export const typography = {
  family: 'Dastkhat, Tahoma, "Segoe UI", sans-serif',
  roles: {
    'heading-1': { size: '1.875rem', weight: fontWeights.semibold, lineHeight: 1.45 },
    'heading-2': { size: '1.375rem', weight: fontWeights.semibold, lineHeight: 1.5 },
    'heading-3': { size: '1.0625rem', weight: fontWeights.medium, lineHeight: 1.55 },
    'body-large': { size: '1rem', weight: fontWeights.regular, lineHeight: 1.7 },
    body: { size: '0.9375rem', weight: fontWeights.regular, lineHeight: 1.75 },
    secondary: { size: '0.875rem', weight: fontWeights.regular, lineHeight: 1.7 },
    caption: { size: '0.75rem', weight: fontWeights.regular, lineHeight: 1.6 },
    control: { size: '0.875rem', weight: fontWeights.semibold, lineHeight: 1.5 },
    action: { size: '0.875rem', weight: fontWeights.medium, lineHeight: 1.5 },
    'control-input': { size: '0.875rem', weight: fontWeights.regular, lineHeight: 10 / 7 },
    label: { size: '0.8125rem', weight: fontWeights.medium, lineHeight: 1.6 },
    navigation: { size: '0.9375rem', weight: fontWeights.regular, lineHeight: 1.5 },
    table: { size: '0.875rem', weight: fontWeights.regular, lineHeight: 1.6 },
    'table-compact': { size: '0.8125rem', weight: fontWeights.regular, lineHeight: 1.6 },
    kpi: { size: '2rem', weight: fontWeights.semibold, lineHeight: 1.3 },
    technical: { size: '0.8125rem', weight: fontWeights.regular, lineHeight: 1.6 },
  } as const satisfies Readonly<Record<string, TextStyle>>,
} as const

export type TypographyRole = keyof typeof typography.roles

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
    'heading-1': { size: '2rem', weight: fontWeights.bold, lineHeight: 1.4 },
    'heading-2': { size: '1.375rem', weight: fontWeights.bold, lineHeight: 1.5 },
    'heading-3': { size: '1.125rem', weight: fontWeights.semibold, lineHeight: 1.55 },
    'body-large': { size: '1rem', weight: fontWeights.regular, lineHeight: 1.75 },
    body: { size: '0.9375rem', weight: fontWeights.regular, lineHeight: 1.75 },
    secondary: { size: '0.875rem', weight: fontWeights.regular, lineHeight: 1.7 },
    caption: { size: '0.75rem', weight: fontWeights.regular, lineHeight: 1.6 },
    control: { size: '0.875rem', weight: fontWeights.semibold, lineHeight: 1.5 },
    table: { size: '0.875rem', weight: fontWeights.regular, lineHeight: 1.6 },
    'table-compact': { size: '0.8125rem', weight: fontWeights.regular, lineHeight: 1.6 },
    kpi: { size: '2rem', weight: fontWeights.bold, lineHeight: 1.25 },
    technical: { size: '0.8125rem', weight: fontWeights.medium, lineHeight: 1.5 },
  } as const satisfies Readonly<Record<string, TextStyle>>,
} as const

export type TypographyRole = keyof typeof typography.roles

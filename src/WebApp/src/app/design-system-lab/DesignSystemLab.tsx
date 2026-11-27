import { lazy, Suspense } from 'react'
import { primitiveColors } from '../../shared/design-system/tokens/primitives'
import type { ColorRole, HexColor, ThemeName } from '../../shared/design-system/tokens/theme-contract'
import { colorVariableName } from '../../shared/design-system/theme/css-variables'
import { useDidrahTheme } from '../../shared/design-system/theme/DidrahThemeProvider'
import { AntSpecimens } from './AntSpecimens'
import { LuminousChatComposerSpecimen } from './LuminousChatComposerSpecimen'
import { NavigationHistorySpecimen } from './NavigationHistorySpecimen'
import { PatternSpecimens } from './PatternSpecimens'
import { TypographySpecimens } from './TypographySpecimens'
import { WelcomeProfileSpecimen } from './WelcomeProfileSpecimen'
import './design-system-lab.css'

const VisualizationSpecimens = lazy(() => import('./VisualizationSpecimens'))
const themeOptions = { dark: 'تیره', light: 'روشن' } satisfies Record<ThemeName, string>
const themeNames = ['dark', 'light'] as const
const surfaceRoles = [
  ['canvas', 'بوم'],
  ['surface-base', 'سطح پایه'],
  ['surface-raised', 'سطح برجسته'],
  ['surface-overlay', 'سطح شناور'],
  ['surface-selected', 'سطح انتخاب‌شده'],
  ['surface-input', 'سطح ورودی'],
] as const satisfies readonly (readonly [ColorRole, string])[]
const textRoles = ['text-primary', 'text-secondary', 'text-muted'] as const
const brandRoles = ['brand-primary', 'brand-on-primary', 'brand-indigo', 'brand-cyan', 'accent-cyan-content'] as const
const interactionRoles = ['border-subtle', 'border-control', 'focus-ring'] as const
const statusRoles = [
  ['status-success', 'موفقیت'],
  ['status-warning', 'هشدار'],
  ['status-critical', 'خطا'],
  ['status-information', 'اطلاع'],
] as const satisfies readonly (readonly [ColorRole, string])[]

function SpecimenValue({ name, value }: { name: string; value: HexColor }) {
  return (
    <span className="lab-token-value" dir="ltr" lang="en">
      <code>{name}</code>
      <code>{value}</code>
    </span>
  )
}

function TokenChip({ role, label }: { role: ColorRole; label?: string }) {
  const { colors } = useDidrahTheme()

  return (
    <li className="lab-token-chip">
      <span
        className="lab-token-color"
        style={{ backgroundColor: `var(${colorVariableName(role)})` }}
        aria-hidden="true"
      />
      {label && <span className="lab-status-label">{label}</span>}
      <SpecimenValue name={role} value={colors[role]} />
    </li>
  )
}

function SurfaceSamples() {
  const { colors } = useDidrahTheme()

  return (
    <ol className="lab-surface-list">
      {surfaceRoles.map(([role, label]) => (
        <li
          className="lab-surface-row"
          key={role}
          style={{ backgroundColor: `var(${colorVariableName(role)})` }}
        >
          <span>{label}</span>
          <SpecimenValue name={role} value={colors[role]} />
        </li>
      ))}
    </ol>
  )
}

export default function DesignSystemLab() {
  const { theme, setTheme } = useDidrahTheme()

  return (
    <main className="design-system-lab">
      <div className="lab-frame">
        <header className="lab-header">
          <div>
            <p className="lab-brand" lang="en" dir="ltr">DIDRAH <span> / Design System</span></p>
            <h1>آزمایشگاه سیستم طراحی</h1>
            <p className="lab-description">اجزای رابط، تایپوگرافی و پالت دیدراه را در دو پوسته بررسی کنید.</p>
          </div>
          <div className="lab-theme-control" role="group" aria-label="پوستهٔ رنگی">
            {themeNames.map((option) => (
              <button
                aria-pressed={theme === option}
                key={option}
                type="button"
                onClick={() => setTheme(option)}
              >
                {themeOptions[option]}
              </button>
            ))}
          </div>
        </header>

        <WelcomeProfileSpecimen />
        <Suspense fallback={<p role="status">در حال آماده‌سازی نمونه‌های تصویری…</p>}>
          <VisualizationSpecimens />
        </Suspense>
        <NavigationHistorySpecimen />
        <PatternSpecimens />
        <AntSpecimens />
        <TypographySpecimens />

        <div className="lab-grid">
          <section className="lab-panel">
            <h2>سلسله‌مراتب سطوح</h2>
            <SurfaceSamples />
          </section>

          <section className="lab-panel">
            <h2>متن و هویت رنگی</h2>
            <div className="lab-type-preview">
              <strong>نمای کلی دیدراه</strong>
              <span>متن ثانویه برای شرح و جزئیات</span>
              <span>یادداشت با تأکید کمتر</span>
              <span className="lab-brand-sample">متن روی آبی اصلی</span>
            </div>
            <ul className="lab-token-list">
              {[...textRoles, ...brandRoles].map((role) => <TokenChip key={role} role={role} />)}
            </ul>
          </section>

          <section className="lab-panel">
            <h2>حاشیه و تمرکز</h2>
            <div className="lab-line-previews" aria-hidden="true">
              <span className="lab-subtle-preview" />
              <span className="lab-control-preview" />
              <span className="lab-focus-preview" />
            </div>
            <ul className="lab-token-list">
              {interactionRoles.map((role) => <TokenChip key={role} role={role} />)}
            </ul>
          </section>

          <section className="lab-panel">
            <h2>رنگ‌های وضعیت</h2>
            <ul className="lab-token-list lab-status-list">
              {statusRoles.map(([role, label]) => <TokenChip key={role} role={role} label={label} />)}
            </ul>
          </section>
        </div>

        <section className="lab-panel lab-primitives">
          <h2>رنگ‌های پایه</h2>
          <ul className="lab-primitive-grid">
            {Object.entries(primitiveColors).map(([name, value]) => (
              <li key={name}>
                <span
                  className="lab-primitive-color"
                  style={{ backgroundColor: value }}
                  aria-hidden="true"
                />
                <SpecimenValue name={name} value={value} />
              </li>
            ))}
          </ul>
        </section>

        <LuminousChatComposerSpecimen />
      </div>
    </main>
  )
}

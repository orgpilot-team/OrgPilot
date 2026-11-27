import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { primitiveColors } from '../../shared/design-system/tokens/primitives'
import type { ColorRole, HexColor, ThemeName } from '../../shared/design-system/tokens/theme-contract'
import { colorVariableName } from '../../shared/design-system/theme/css-variables'
import { useDidrahTheme } from '../../shared/design-system/theme/DidrahThemeProvider'
import { ButtonFieldSpecimens, DataFeedbackSpecimens, OverlaySpecimens, SelectionSpecimens } from './AntSpecimens'
import { LuminousChatComposerSpecimen } from './LuminousChatComposerSpecimen'
import { NavigationHistorySpecimen } from './NavigationHistorySpecimen'
import { InsightSpecimen, NavigationPatternSpecimen, ReviewStateSpecimen } from './PatternSpecimens'
import { PrimaryNavigationSpecimen } from './PrimaryNavigationSpecimen'
import { TypographySpecimens } from './TypographySpecimens'
import { ChartCatalogSpecimen, WorkflowCatalogSpecimen } from './VisualizationSpecimens'
import { WelcomeProfileSpecimen } from './WelcomeProfileSpecimen'
import './design-system-lab.css'

const themeOptions = { dark: 'تیره', light: 'روشن' } satisfies Record<ThemeName, string>
const themeNames = ['dark', 'light'] as const
const sections = {
  foundations: 'مبانی طراحی',
  typography: 'تایپوگرافی',
  'buttons-fields': 'دکمه‌ها و فیلدها',
  selection: 'کنترل‌های انتخاب',
  overlays: 'پنجره‌ها و راهنماها',
  navigation: 'ناوبری و پوسته',
  assistant: 'دستیار هوش مصنوعی',
  'data-feedback': 'داده و بازخورد',
  insights: 'شاخص‌ها و بینش‌ها',
  charts: 'نمودارها',
  workflow: 'گردش کار',
  validation: 'کنترل‌های اعتبارسنجی',
} as const

type SectionId = keyof typeof sections

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

function CatalogSection({ id, headingId = `${id}-heading`, children }: {
  id: SectionId
  headingId?: string
  children: ReactNode
}) {
  return (
    <section id={id} className="lab-catalog-section" aria-labelledby={headingId} tabIndex={-1}>
      <h2 id={headingId}>{sections[id]}</h2>
      {children}
    </section>
  )
}

function CatalogSidebar() {
  const { theme, setTheme } = useDidrahTheme()
  const [activeSection, setActiveSection] = useState<string>()

  useEffect(() => {
    const getTarget = () => document.getElementById(window.location.hash.slice(1))
    const updateCurrentSection = () => setActiveSection(getTarget()?.closest('.lab-catalog-section')?.id)

    // The development route loads after the browser's first fragment lookup.
    getTarget()?.scrollIntoView()
    updateCurrentSection()
    window.addEventListener('hashchange', updateCurrentSection)
    return () => window.removeEventListener('hashchange', updateCurrentSection)
  }, [])

  return (
    <aside className="lab-sidebar">
      <div className="lab-theme-control lab-catalog-theme" role="group" aria-label="پوستهٔ رنگی">
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
      <nav className="lab-section-index" aria-label="بخش‌های سیستم طراحی">
        <ul>
          {Object.entries(sections).map(([id, label]) => (
            <li key={id}>
              <a href={`#${id}`} aria-current={activeSection === id ? 'location' : undefined}>{label}</a>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}

function FoundationSpecimens() {
  return (
    <>
      <div className="lab-grid">
        <section className="lab-panel">
          <h3>سلسله‌مراتب سطوح</h3>
          <SurfaceSamples />
        </section>

        <section className="lab-panel">
          <h3>متن و هویت رنگی</h3>
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
          <h3>حاشیه و تمرکز</h3>
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
          <h3>رنگ‌های وضعیت</h3>
          <ul className="lab-token-list lab-status-list">
            {statusRoles.map(([role, label]) => <TokenChip key={role} role={role} label={label} />)}
          </ul>
        </section>
      </div>

      <section className="lab-panel">
        <h3>رنگ‌های پایه</h3>
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
    </>
  )
}

export default function DesignSystemLab() {
  return (
    <div className="design-system-lab">
      <a className="lab-skip-link" href="#lab-content">رفتن به نمونه‌ها</a>
      <div className="lab-frame">
        <header className="lab-header">
          <p className="lab-brand" lang="en" dir="ltr">DIDRAH</p>
          <h1>آزمایشگاه سیستم طراحی</h1>
        </header>

        <div className="lab-layout">
          <CatalogSidebar />
          <main className="lab-catalog" id="lab-content" tabIndex={-1}>
            <CatalogSection id="foundations"><FoundationSpecimens /></CatalogSection>
            <CatalogSection id="typography"><TypographySpecimens /></CatalogSection>
            <CatalogSection id="buttons-fields" headingId="lab-ant-heading"><ButtonFieldSpecimens /></CatalogSection>
            <CatalogSection id="selection"><SelectionSpecimens /></CatalogSection>
            <CatalogSection id="overlays"><OverlaySpecimens /></CatalogSection>
            <CatalogSection id="navigation">
              <div className="lab-shell-grid">
                <WelcomeProfileSpecimen />
                <PrimaryNavigationSpecimen />
              </div>
              <NavigationHistorySpecimen />
              <NavigationPatternSpecimen />
            </CatalogSection>
            <CatalogSection id="assistant"><LuminousChatComposerSpecimen /></CatalogSection>
            <CatalogSection id="data-feedback"><DataFeedbackSpecimens /></CatalogSection>
            <CatalogSection id="insights" headingId="lab-pattern-heading"><InsightSpecimen /></CatalogSection>
            <CatalogSection id="charts" headingId="lab-visualization-heading"><ChartCatalogSpecimen /></CatalogSection>
            <CatalogSection id="workflow"><WorkflowCatalogSpecimen /></CatalogSection>
            <CatalogSection id="validation"><ReviewStateSpecimen /></CatalogSection>
          </main>
        </div>
      </div>
    </div>
  )
}

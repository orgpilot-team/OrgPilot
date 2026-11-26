import type { ReactNode } from 'react'
import './patterns.css'

type PanelProps = {
  children: ReactNode
  surface?: 'base' | 'raised' | 'overlay' | 'selected'
  density?: 'regular' | 'compact'
}

export function Panel({ children, surface = 'base', density = 'regular' }: PanelProps) {
  return <div className="didrah-panel" data-surface={surface} data-density={density}>{children}</div>
}

type SectionHeaderProps = {
  title: ReactNode
  description?: ReactNode
  actions?: ReactNode
  level?: 2 | 3 | 4
  id?: string
}

export function SectionHeader({ title, description, actions, level = 3, id }: SectionHeaderProps) {
  const Heading = `h${level}` as const

  return (
    <header className="didrah-section-header">
      <div>
        <Heading id={id}>{title}</Heading>
        {description && <p>{description}</p>}
      </div>
      {actions && <div className="didrah-section-actions">{actions}</div>}
    </header>
  )
}

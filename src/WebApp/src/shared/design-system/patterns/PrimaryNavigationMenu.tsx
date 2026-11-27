import type { ReactNode } from 'react'
import './primary-navigation-menu.css'

export type PrimaryNavigationItem = Readonly<{
  id: string
  label: string
  /** A decorative icon. The label gives the button its accessible name. */
  icon: ReactNode
  disabled?: boolean
}>

export type PrimaryNavigationMenuProps = Readonly<{
  items: readonly PrimaryNavigationItem[]
  activeItemId: string | null
  onNavigate: (itemId: string) => void
  ariaLabel?: string
}>

export function PrimaryNavigationMenu({
  items, activeItemId, onNavigate, ariaLabel = 'ناوبری اصلی',
}: PrimaryNavigationMenuProps) {
  return (
    <nav className="didrah-primary-nav" aria-label={ariaLabel} dir="rtl" lang="fa">
      {items.length === 0 ? (
        <p className="didrah-primary-nav-empty" role="status">گزینه‌ای برای ناوبری وجود ندارد.</p>
      ) : (
        <ul className="didrah-primary-nav-list" role="list">
          {items.map(({ id, label, icon, disabled }) => (
            <li key={id}>
              <button
                type="button"
                className="didrah-primary-nav-item"
                aria-current={id === activeItemId ? 'page' : undefined}
                disabled={disabled}
                onClick={() => onNavigate(id)}
              >
                <span className="didrah-primary-nav-icon" aria-hidden="true">{icon}</span>
                <bdi className="didrah-primary-nav-label">{label}</bdi>
              </button>
            </li>
          ))}
        </ul>
      )}
    </nav>
  )
}

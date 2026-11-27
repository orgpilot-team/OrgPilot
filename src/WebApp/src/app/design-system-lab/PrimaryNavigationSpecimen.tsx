import { useState } from 'react'
import { SectionHeader } from '../../shared/design-system/patterns/Panel'
import { PrimaryNavigationMenu } from '../../shared/design-system/patterns/PrimaryNavigationMenu'
import type { PrimaryNavigationItem } from '../../shared/design-system/patterns/PrimaryNavigationMenu'
import './primary-navigation-specimen.css'

const iconPaths = {
  overview: 'M4.5 2.5h4.4a2 2 0 0 1 2 2v4.4a2 2 0 0 1-2 2H4.5a2 2 0 0 1-2-2V4.5a2 2 0 0 1 2-2Zm10.6 0h4.4a2 2 0 0 1 2 2v4.4a2 2 0 0 1-2 2h-4.4a2 2 0 0 1-2-2V4.5a2 2 0 0 1 2-2ZM4.5 13.1h4.4a2 2 0 0 1 2 2v4.4a2 2 0 0 1-2 2H4.5a2 2 0 0 1-2-2v-4.4a2 2 0 0 1 2-2Zm10.6 0h4.4a2 2 0 0 1 2 2v4.4a2 2 0 0 1-2 2h-4.4a2 2 0 0 1-2-2v-4.4a2 2 0 0 1 2-2Z',
  assistant: 'M10.8 2.1a1.2 1.2 0 0 1 2.4 0c1.1 6 2.6 7.5 8.7 8.7a1.2 1.2 0 0 1 0 2.4c-6.1 1.2-7.6 2.7-8.7 8.7a1.2 1.2 0 0 1-2.4 0c-1.1-6-2.6-7.5-8.7-8.7a1.2 1.2 0 0 1 0-2.4c6.1-1.2 7.6-2.7 8.7-8.7Z',
  accounts: 'M21 4H4a2 2 0 0 0 0 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6m14.5 8.5h2',
  transactions: 'M21 6.5H3m4-4-4 4 4 4M3 17.5h18m-4-4 4 4-4 4',
  reports: 'M10 2.6A10 10 0 1 0 21.8 14H10V2.6Zm3.2-.6v9h8.9A10 10 0 0 0 13.2 2ZM10 14l-6.9 4.2M10 11.3l-8 4.8',
  sales: 'M2.5 2.5v19h19m-16-5.1 5.6-5.5 3.5 3 5.9-7.7m-5.5 0h5.5v5.5',
  branches: 'M1 9h22L12 2 1 9Zm2 10h18M1 22h22M5 12v7m4.7-7v7m4.6-7v7m4.7-7v7',
  calculator: 'M4 2h16v20H4zM7.5 7.2h9M7.5 11.5h.5m3.8 0h.4m3.8 0h.5m-9 3.4h.5m3.8 0h.4m3.8 0h.5m-9 3.4h.5m3.8 0h.4m3.8 0h.5',
} as const

function NavigationIcon({ name }: { name: keyof typeof iconPaths }) {
  const filled = name === 'assistant'

  return (
    <svg viewBox="0 0 24 24" focusable="false">
      <path
        d={iconPaths[name]}
        fill={filled ? 'currentColor' : 'none'}
        stroke={filled ? 'none' : 'currentColor'}
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

const navigationItems = [
  { id: 'overview', label: 'نمای کلی', icon: <NavigationIcon name="overview" /> },
  { id: 'assistant', label: 'دستیار دیدراه', icon: <NavigationIcon name="assistant" /> },
  { id: 'accounts', label: 'حساب‌ها', icon: <NavigationIcon name="accounts" /> },
  { id: 'transactions', label: 'تراکنش‌ها', icon: <NavigationIcon name="transactions" /> },
  { id: 'reports', label: 'گزارش‌ها', icon: <NavigationIcon name="reports" /> },
  { id: 'sales', label: 'روند فروش', icon: <NavigationIcon name="sales" /> },
  { id: 'branches', label: 'شعبه‌ها', icon: <NavigationIcon name="branches" /> },
  { id: 'calculator', label: 'محاسبه‌گر', icon: <NavigationIcon name="calculator" />, disabled: true },
] satisfies readonly PrimaryNavigationItem[]

export function PrimaryNavigationSpecimen() {
  const [activeItemId, setActiveItemId] = useState('assistant')
  const [showItems, setShowItems] = useState(true)
  const items = showItems ? navigationItems : []
  const activeItem = items.find((item) => item.id === activeItemId)

  return (
    <section className="lab-primary-navigation" aria-labelledby="lab-primary-navigation-heading">
      <SectionHeader id="lab-primary-navigation-heading" level={2} title="منوی ناوبری اصلی" />
      <div className="lab-primary-navigation-stage">
        <PrimaryNavigationMenu items={items} activeItemId={activeItemId} onNavigate={setActiveItemId} />
        <div className="lab-primary-navigation-controls">
          <div role="status">{activeItem && <p>بخش فعال: <bdi>{activeItem.label}</bdi></p>}</div>
          <label>
            <input type="checkbox" checked={showItems} onChange={(event) => setShowItems(event.target.checked)} />
            نمایش گزینه‌ها
          </label>
        </div>
      </div>
    </section>
  )
}

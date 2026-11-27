import { useState } from 'react'
import { NavigationHistorySidebar } from '../../shared/design-system/patterns/NavigationHistorySidebar'
import type { NavigationHistoryGroup } from '../../shared/design-system/patterns/NavigationHistorySidebar'
import { Panel, SectionHeader } from '../../shared/design-system/patterns/Panel'
import './navigation-history-specimen.css'

const initialGroups = [
  { id: 'today', label: 'امروز', items: [
    { id: 'annual-sales', title: 'فروش سالانه' },
  ] },
  { id: 'yesterday', label: 'دیروز', items: [
    { id: 'weekly-target', title: 'هدف فروش هفته' },
    { id: 'branch-comparison', title: 'مقایسهٔ فروش شعب' },
    { id: 'stock-shortage', title: 'کمبود موجودی' },
    { id: 'order-delay', title: 'تأخیر سفارش‌ها' },
  ] },
  { id: 'last-week', label: '۷ روز گذشته', items: [
    { id: 'category-sales', title: 'فروش گروه‌های کالا' },
    { id: 'profit-margin', title: 'حاشیهٔ سود کالا' },
    { id: 'store-returns', title: 'مرجوعی فروشگاه‌ها' },
    { id: 'supplier-stock', title: 'موجودی تأمین‌کننده' },
    { id: 'long-title', title: 'بررسی فروش کالاهای پرفروش و کمبود موجودی در شعب شمال و غرب در هفتهٔ گذشته' },
  ] },
] satisfies readonly NavigationHistoryGroup[]

export function NavigationHistorySpecimen() {
  const [groups, setGroups] = useState<readonly NavigationHistoryGroup[]>(initialGroups)
  const [activeItemId, setActiveItemId] = useState<string | null>('annual-sales')
  const [draftCount, setDraftCount] = useState(0)
  const [showSettings, setShowSettings] = useState(false)
  const activeItem = groups.flatMap((group) => group.items).find((item) => item.id === activeItemId)

  function newChat() {
    const count = draftCount + 1
    const item = { id: `draft-${count}`, title: `گفت‌وگوی تازهٔ ${count.toLocaleString('fa-IR')}` }
    setDraftCount(count)
    setGroups((current) => {
      const today = current.find((group) => group.id === 'today')

      return [
        { id: 'today', label: 'امروز', items: [item, ...(today?.items ?? [])] },
        ...current.filter((group) => group.id !== 'today'),
      ]
    })
    setActiveItemId(item.id)
  }

  function deleteChat(itemId: string) {
    setGroups((current) => current.map((group) => ({
      ...group,
      items: group.items.filter((item) => item.id !== itemId),
    })))
    setActiveItemId((current) => current === itemId ? null : current)
  }

  function setHistory(nextGroups: readonly NavigationHistoryGroup[]) {
    setGroups(nextGroups)
    setActiveItemId(nextGroups.length ? 'annual-sales' : null)
  }

  return (
    <section className="lab-history-specimen" aria-labelledby="lab-history-heading">
      <Panel>
        <SectionHeader id="lab-history-heading" level={2} title="نوار کناری تاریخچهٔ گفت‌وگوها" />
        <div className="lab-history-stage">
          <NavigationHistorySidebar
            groups={groups}
            activeItemId={activeItemId}
            onSelect={setActiveItemId}
            onDelete={deleteChat}
            onNewChat={newChat}
            onSettings={() => setShowSettings((value) => !value)}
          />
          <div className="lab-history-content">
            <p role="status">{activeItem?.title ?? 'گفت‌وگویی انتخاب نشده است.'}</p>
            {showSettings && (
              <section className="lab-history-settings" aria-labelledby="lab-history-settings-heading">
                <h3 id="lab-history-settings-heading">تنظیمات تاریخچهٔ نمونه</h3>
                <div className="lab-theme-control">
                  <button type="button" onClick={() => setHistory([])}>پاک کردن تاریخچه</button>
                  <button type="button" onClick={() => setHistory(initialGroups)}>بازنشانی تاریخچه</button>
                </div>
              </section>
            )}
          </div>
        </div>
      </Panel>
    </section>
  )
}

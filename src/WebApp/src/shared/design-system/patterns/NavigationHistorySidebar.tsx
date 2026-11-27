import { useId, useLayoutEffect, useRef, useState } from 'react'
import type { MouseEvent } from 'react'
import './navigation-history-sidebar.css'

export type NavigationHistoryItem = Readonly<{ id: string; title: string }>

export type NavigationHistoryGroup = Readonly<{
  id: string
  label: string
  items: readonly NavigationHistoryItem[]
}>

export type NavigationHistorySidebarProps = Readonly<{
  groups: readonly NavigationHistoryGroup[]
  activeItemId: string | null
  onSelect: (itemId: string) => void
  onDelete: (itemId: string) => void
  onNewChat: () => void
  onSettings: () => void
}>

const iconPaths = {
  chat: 'M5.4 4.2h25.2q1.2 0 1.2 1.2v17.8l-8.9 8.9H5.4q-1.4 0-1.4-1.4V5.6q0-1.4 1.4-1.4ZM22.9 32.1v-8.9h8.9M12 12.5h10M12 17.6h10M12 22.6h5.5',
  delete: 'M4.5 6.5h27M7 6.5v23.8q0 1.6 1.6 1.6h18.8q1.6 0 1.6-1.6V6.5M12 6.5V4a2.6 2.6 0 0 1 2.6-2.6h6.8A2.6 2.6 0 0 1 24 4v2.5M14 13v12M22 13v12',
  plus: 'M18 4v28M4 18h28',
  search: 'M29.2 16.1a13.1 13.1 0 1 1-26.2 0 13.1 13.1 0 0 1 26.2 0Zm-3.7 9.4 8 8',
  settings: 'M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.38a2 2 0 0 0-.73-2.73l-.15-.09a2 2 0 0 1-1-1.74v-.51a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2Z',
  close: 'm9 9 18 18M27 9 9 27',
} as const

/* Settings gear adapted from Lucide. https://lucide.dev/license
ISC License
Copyright (c) 2026 Lucide Icons and Contributors

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/
function SidebarIcon({ name }: { name: keyof typeof iconPaths }) {
  if (name === 'settings') {
    return (
      <svg className="didrah-history-icon" viewBox="0 0 24 24" aria-hidden="true">
        <g fill="none" stroke="currentColor" strokeWidth="1.65" strokeLinecap="round" strokeLinejoin="round">
          <path d={iconPaths.settings} transform="rotate(30 12 12)" />
          <circle cx="12" cy="12" r="4" />
        </g>
      </svg>
    )
  }

  return (
    <svg className="didrah-history-icon" viewBox="0 0 36 36" aria-hidden="true">
      <path d={iconPaths[name]} fill="none" stroke="currentColor" strokeWidth="2.45" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function ActiveHistoryDetail() {
  const id = useId()
  const accent = `${id}-accent`
  const curve = `${id}-curve`
  const dot = `${id}-dot`
  const glow = `${id}-glow`
  const dotGlow = `${id}-dot-glow`

  return (
    <svg className="didrah-history-active-detail" viewBox="0 0 144 72" aria-hidden="true">
      <defs>
        <path id={curve} d="M47.5 0A23 23 0 0 1 70.5 23V49A23 23 0 0 1 47.5 72" />
        <linearGradient className="didrah-history-accent-ink" id={accent} x1="0" y1="0" x2="0" y2="72" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopOpacity="0" />
          <stop offset=".12" stopOpacity=".08" />
          <stop offset=".20" stopOpacity=".3" />
          <stop offset=".31" stopOpacity=".68" />
          <stop offset=".69" stopOpacity=".68" />
          <stop offset=".80" stopOpacity=".3" />
          <stop offset=".88" stopOpacity=".08" />
          <stop offset="1" stopOpacity="0" />
        </linearGradient>
        <radialGradient id={dot} cx="60%" cy="38%" r="67%">
          <stop stopColor="#6393ff" />
          <stop offset="47%" stopColor="#4979f5" />
          <stop offset="100%" stopColor="#2144b9" />
        </radialGradient>
        <filter id={glow} x="-100%" y="-25%" width="300%" height="150%">
          <feGaussianBlur stdDeviation="1.65" />
        </filter>
        <filter id={dotGlow} x="-60%" y="-60%" width="220%" height="220%">
          <feGaussianBlur stdDeviation="1.45" />
        </filter>
      </defs>
      <path className="didrah-history-selected-fill" d="M48 0A24 24 0 0 1 72 24V48A24 24 0 0 1 48 72H144V0Z" />
      <path className="didrah-history-delete-fill" d="M48 0A24 24 0 0 1 72 24V48A24 24 0 0 1 48 72H106A36 36 0 0 0 106 0Z" />
      <use href={`#${curve}`} fill="none" stroke={`url(#${accent})`} strokeWidth="5.5" opacity=".42" filter={`url(#${glow})`} />
      <use href={`#${curve}`} fill="none" stroke={`url(#${accent})`} strokeWidth="2.7" />
      <circle cx="36" cy="36" r="8.6" fill="#1c4bea" opacity=".43" filter={`url(#${dotGlow})`} />
      <circle cx="36" cy="36" r="8" fill={`url(#${dot})`} />
    </svg>
  )
}

function normalizeSearch(text: string) {
  return text.normalize('NFKC').toLocaleLowerCase('fa')
    .replace(/[يى]/g, 'ی').replace(/ك/g, 'ک')
    .replace(/[\u200c\s]+/g, ' ').trim()
}

export function NavigationHistorySidebar({
  groups, activeItemId, onSelect, onDelete, onNewChat, onSettings,
}: NavigationHistorySidebarProps) {
  const searchId = useId()
  const [searchOpen, setSearchOpen] = useState(false)
  const [query, setQuery] = useState('')
  const searchButton = useRef<HTMLButtonElement>(null)
  const searchField = useRef<HTMLInputElement>(null)
  const frame = useRef<HTMLElement>(null)
  const scroll = useRef<HTMLDivElement>(null)
  const content = useRef<HTMLDivElement>(null)
  const activeRow = useRef<HTMLLIElement>(null)

  const searchText = normalizeSearch(query)
  const visibleGroups = groups.map((group) => ({
    ...group,
    items: group.items.filter((item) => !searchText || normalizeSearch(item.title).includes(searchText)),
  })).filter((group) => group.items.length > 0)

  useLayoutEffect(() => {
    if (searchOpen) searchField.current?.focus()
  }, [searchOpen])

  useLayoutEffect(() => {
    const history = frame.current!
    const viewport = scroll.current!
    const rows = content.current!

    // The background extends past the scroll viewport so each return has space at the list edges.
    function syncSurface() {
      const row = activeRow.current
      const more = viewport.scrollHeight - viewport.clientHeight - viewport.scrollTop > 1
      const rowBounds = row?.getBoundingClientRect()
      const viewportBounds = viewport.getBoundingClientRect()
      const visible = rowBounds && rowBounds.bottom > viewportBounds.top && rowBounds.top < viewportBounds.bottom

      if (visible) {
        history.style.setProperty('--history-active-y', `${rowBounds.top - history.getBoundingClientRect().top}px`)
      }
      history.toggleAttribute('data-has-active', Boolean(visible))
      viewport.toggleAttribute('data-more', more)
    }

    syncSurface()
    const observer = new ResizeObserver(syncSurface)
    observer.observe(viewport)
    observer.observe(rows)
    viewport.addEventListener('scroll', syncSurface, { passive: true })

    return () => {
      observer.disconnect()
      viewport.removeEventListener('scroll', syncSurface)
    }
  }, [groups, activeItemId, searchText, searchOpen])

  function closeSearch() {
    setQuery('')
    setSearchOpen(false)
    searchButton.current?.focus()
  }

  function deleteItem(event: MouseEvent<HTMLButtonElement>, itemId: string) {
    if (event.currentTarget === document.activeElement) {
      const buttons = Array.from(content.current!.querySelectorAll<HTMLButtonElement>('.didrah-history-select'))
      const selected = buttons.findIndex((button) => button.getAttribute('aria-current') === 'true')
      const next = buttons[selected + 1] ?? buttons[selected - 1] ?? searchButton.current
      next?.focus()
    }
    onDelete(itemId)
  }

  return (
    <aside className="didrah-history-sidebar" dir="rtl" lang="fa" aria-label="دستیار دیدراه">
      <header className="didrah-history-header">
        <p className="didrah-history-brand">دیدراه <span>هوش مصنوعی</span></p>
        <div className="didrah-history-actions">
          <button className="didrah-history-action didrah-history-new" type="button" onClick={() => {
            if (searchOpen) {
              setQuery('')
              setSearchOpen(false)
            }
            if (scroll.current) scroll.current.scrollTop = 0
            onNewChat()
          }}>
            <SidebarIcon name="plus" /> گفت‌وگوی تازه
          </button>
          <button
            className="didrah-history-search"
            type="button"
            ref={searchButton}
            aria-label="جست‌وجوی گفت‌وگوها"
            aria-expanded={searchOpen}
            aria-controls={searchId}
            onClick={() => searchOpen ? closeSearch() : setSearchOpen(true)}
          >
            <SidebarIcon name="search" />
          </button>
        </div>
        <div className="didrah-history-search-form" role="search" id={searchId} hidden={!searchOpen} onKeyDown={(event) => {
          if (event.key === 'Escape' && !event.nativeEvent.isComposing) {
            event.preventDefault()
            closeSearch()
          }
        }}>
          <input
            ref={searchField}
            type="search"
            aria-label="عنوان گفت‌وگو"
            placeholder="عنوان گفت‌وگو"
            value={query}
            onChange={(event) => {
              if (scroll.current) scroll.current.scrollTop = 0
              setQuery(event.target.value)
            }}
          />
          <button type="button" aria-label="بستن جست‌وجو" onClick={closeSearch}><SidebarIcon name="close" /></button>
        </div>
      </header>

      <nav className="didrah-history-frame" aria-label="تاریخچهٔ گفت‌وگوها" ref={frame}>
        <div className="didrah-history-scroll" ref={scroll}>
          <div className="didrah-history-content" ref={content}>
            {visibleGroups.length === 0 && (
              <p className="didrah-history-empty" role="status">
                {groups.some((group) => group.items.length > 0) ? 'گفت‌وگویی پیدا نشد.' : 'هنوز گفت‌وگویی ندارید.'}
              </p>
            )}
            {visibleGroups.map((group) => (
              <div className="didrah-history-group" key={group.id}>
                <h3>{group.label}</h3>
                <ul>
                  {group.items.map((item) => {
                    const active = item.id === activeItemId

                    return (
                      <li className="didrah-history-row" key={item.id} ref={active ? activeRow : undefined}>
                        {active && <ActiveHistoryDetail />}
                        <button
                          className="didrah-history-select"
                          type="button"
                          aria-current={active ? 'true' : undefined}
                          title={item.title}
                          onClick={() => onSelect(item.id)}
                        >
                          <SidebarIcon name="chat" />
                          <bdi>{item.title}</bdi>
                        </button>
                        {active && (
                          <button
                            className="didrah-history-delete"
                            type="button"
                            aria-label={`حذف گفت‌وگو: ${item.title}`}
                            onClick={(event) => deleteItem(event, item.id)}
                          >
                            <SidebarIcon name="delete" />
                          </button>
                        )}
                      </li>
                    )
                  })}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </nav>

      <footer className="didrah-history-footer">
        <div>
          <button className="didrah-history-action didrah-history-settings" type="button" onClick={onSettings}>
            <SidebarIcon name="settings" /> تنظیمات
          </button>
        </div>
      </footer>
    </aside>
  )
}

import { useId, useState } from 'react'
import { useDidrahTheme } from '../theme/DidrahThemeProvider'
import { Panel } from './Panel'
import './welcome-profile-card.css'

export type WelcomeProfileCardProps = {
  managerName: string
  avatarSrc?: string
  /** A valid Date. The card uses the local day in Tehran. */
  date: Date
}

const persianDate = new Intl.DateTimeFormat('fa-IR', {
  calendar: 'persian',
  numberingSystem: 'arabext',
  timeZone: 'Asia/Tehran',
  weekday: 'long',
  day: 'numeric',
  month: 'long',
})

function ProfileAvatar({ src, initial }: { src?: string; initial: string }) {
  const [loaded, setLoaded] = useState(false)

  return (
    <span className="didrah-welcome-avatar" aria-hidden="true">
      {!loaded && <span>{initial}</span>}
      {src && (
        <img
          alt=""
          src={src}
          data-loaded={loaded}
          onLoad={() => setLoaded(true)}
          onError={() => setLoaded(false)}
        />
      )}
    </span>
  )
}

export function WelcomeProfileCard({ managerName, avatarSrc, date }: WelcomeProfileCardProps) {
  const headingId = useId()
  const { theme, setTheme } = useDidrahTheme()
  const name = managerName.trim() || 'مدیر'
  const src = avatarSrc?.trim() || undefined
  const [initial] = name

  return (
    <section className="didrah-welcome-profile" lang="fa" dir="rtl" aria-labelledby={headingId}>
      <Panel>
        <div className="didrah-welcome-top">
          <ProfileAvatar key={src} src={src} initial={initial} />
          <div className="didrah-welcome-theme" role="group" aria-label="پوستهٔ رنگی">
            <button type="button" aria-label="حالت تیره" aria-pressed={theme === 'dark'} onClick={() => setTheme('dark')}>
              <svg viewBox="0 0 36 36" fill="none" aria-hidden="true">
                <path
                  d="M15.5 2.2C8.9 4 4.6 9.9 4.6 16.7c0 8.1 6.1 14.5 14.1 14.5 6.9 0 12.7-4.6 14.5-10.7-5.4 1.7-10.7.3-14.2-3.3-3.7-3.9-4.8-9.6-3.5-15Z"
                  stroke="currentColor"
                  strokeWidth="2.45"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
            <button type="button" aria-label="حالت روشن" aria-pressed={theme === 'light'} onClick={() => setTheme('light')}>
              <svg viewBox="0 0 36 36" fill="none" aria-hidden="true">
                <circle cx="18" cy="18" r="8.6" stroke="currentColor" strokeWidth="2.3" />
                <path
                  d="M18 2.9v1.7m0 26.8v1.7M2.9 18h1.7m26.8 0h1.7M7.3 7.3l1.2 1.2m19 19 1.2 1.2M7.3 28.7l1.2-1.2m19-19 1.2-1.2"
                  stroke="currentColor"
                  strokeWidth="2.3"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          </div>
        </div>
        <time className="didrah-welcome-date" dateTime={date.toISOString()}>{persianDate.format(date)}</time>
        <h2 className="didrah-welcome-heading" id={headingId}>
          خوش آمدید،
          <br />
          <bdi>{name}</bdi>
        </h2>
      </Panel>
    </section>
  )
}

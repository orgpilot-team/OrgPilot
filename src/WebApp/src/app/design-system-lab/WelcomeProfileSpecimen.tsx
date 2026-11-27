import { useState } from 'react'
import { WelcomeProfileCard } from '../../shared/design-system/patterns/WelcomeProfileCard'
import avatar from './welcome-profile-avatar.png'

const managerName = 'آرمان رضایی'
const date = new Date('2025-03-24T07:30:00+03:30')

export function WelcomeProfileSpecimen() {
  const [showAvatar, setShowAvatar] = useState(true)

  return (
    <section className="lab-welcome-profile" aria-label="نمونهٔ کارت خوشامدگویی">
      <WelcomeProfileCard managerName={managerName} avatarSrc={showAvatar ? avatar : undefined} date={date} />
      <label className="lab-welcome-avatar-control">
        <input type="checkbox" checked={showAvatar} onChange={(event) => setShowAvatar(event.target.checked)} />
        نمایش عکس مدیر
      </label>
    </section>
  )
}

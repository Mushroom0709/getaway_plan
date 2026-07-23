import type { Day } from '../types'
import { useIsMobile } from '../hooks/useIsMobile'

interface TopNavProps {
  days: Day[]
  activeDay: string
  onChange: (day: string) => void
}

export default function TopNav({ days, activeDay, onChange }: TopNavProps) {
  const isMobile = useIsMobile()

  return (
    <div className={`flex gap-2 overflow-x-auto pb-2 ${isMobile ? 'px-2' : ''}`}>
      {days.map(day => (
        <button
          key={day.day_number}
          onClick={() => onChange(`D${day.day_number}`)}
          className={`shrink-0 px-3 py-1.5 rounded-lg text-sm font-medium transition ${
            activeDay === `D${day.day_number}`
              ? 'bg-[var(--accent)] text-white'
              : 'bg-[var(--card)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border)]'
          }`}
        >
          {isMobile ? `D${day.day_number}` : day.title || `D${day.day_number}`}
        </button>
      ))}
      <button
        onClick={() => onChange('budget')}
        className={`shrink-0 px-3 py-1.5 rounded-lg text-sm font-medium transition ${
          activeDay === 'budget'
            ? 'bg-[var(--accent)] text-white'
            : 'bg-[var(--card)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border)]'
        }`}
      >
        💰 费用
      </button>
    </div>
  )
}

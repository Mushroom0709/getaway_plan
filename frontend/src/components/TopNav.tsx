import type { Day } from '../types'

interface TopNavProps {
  days: Day[]
  activeDay: string
  onChange: (day: string) => void
}

const iconMap: Record<number, string> = {
  0: '✈️', 1: '🚗', 2: '🚗', 3: '🚗', 4: '🚗', 5: '🚗', 6: '🚗', 7: '🚗',
}

export default function TopNav({ days, activeDay, onChange }: TopNavProps) {
  const sorted = [...days].sort((a, b) => (a.sort_order ?? a.day_number) - (b.sort_order ?? b.day_number))
  return (
    <div className="flex flex-col gap-1 p-2 h-full overflow-y-auto">
      <button
        onClick={() => onChange('all')}
        className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition ${activeDay === 'all'
            ? 'bg-[var(--accent)] text-white'
            : 'bg-[var(--card)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border)]'
          }`}
      >
        🗺️ 全部
      </button>
      {sorted.map(day => (
        <button
          key={day.day_number}
          onClick={() => onChange(`D${day.day_number}`)}
          className={`w-full text-left px-3 py-2 rounded-lg text-sm transition ${activeDay === `D${day.day_number}`
              ? 'bg-[var(--accent)] text-white'
              : 'bg-[var(--card)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border)]'
            }`}
        >
          <div className="font-medium text-xs">D{day.day_number} {iconMap[day.day_number] || ''}</div>
          <div className="text-xs leading-tight opacity-80 mt-0.5 line-clamp-2">{day.title || 'Day ' + day.day_number}</div>
        </button>
      ))}
      <button
        onClick={() => onChange('overview')}
        className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition mt-auto ${activeDay === 'overview'
            ? 'bg-[var(--accent)] text-white'
            : 'bg-[var(--card)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border)]'
          }`}
      >
        📊 总览
      </button>
    </div>
  )
}

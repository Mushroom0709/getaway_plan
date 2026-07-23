import type { Day, Weather } from '../types'

interface DayContentProps {
  day: Day
  weather?: Weather
}

export default function DayContent({ day, weather }: DayContentProps) {
  return (
    <div className="space-y-3">
      <div>
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">
          {day.title || `第 ${day.day_number} 天`}
        </h3>
        {day.date && <p className="text-sm text-[var(--text-secondary)]">{day.date}</p>}
      </div>
      {day.drive_hours !== null && day.drive_hours !== undefined && (
        <div className="flex items-center gap-2 text-sm text-[var(--text-secondary)]">
          <span>🚗</span>
          <span>驾驶约 {day.drive_hours} 小时</span>
        </div>
      )}
      {day.hotel_city && (
        <div className="flex items-center gap-2 text-sm text-[var(--text-secondary)]">
          <span>🏠</span>
          <span>宿 {day.hotel_city}</span>
        </div>
      )}
      {weather && (
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-3 text-sm">
          <div className="text-[var(--text-primary)] font-medium">{weather.city}</div>
          <div className="text-[var(--text-secondary)]">
            {weather.high_temp} / {weather.low_temp} · {weather.weather_desc}
          </div>
          {weather.advice && <div className="text-[var(--text-secondary)] mt-1">{weather.advice}</div>}
        </div>
      )}
    </div>
  )
}

import type { Attraction, SocialNote } from '../types'

interface AttractionDetailProps {
  attraction: Attraction
  notes?: SocialNote[]
  onViewPhotos?: () => void
}

export default function AttractionDetail({ attraction, notes, onViewPhotos }: AttractionDetailProps) {
  return (
    <div className="space-y-4">
      <div>
        {attraction.ticket_price && (
          <div className="text-sm text-[var(--text-secondary)]">🎫 {attraction.ticket_price}</div>
        )}
        {attraction.opening_hours && (
          <div className="text-sm text-[var(--text-secondary)]">🕐 {attraction.opening_hours}</div>
        )}
        {attraction.best_time_of_day && (
          <div className="text-sm text-[var(--text-secondary)]">📸 最佳时间: {attraction.best_time_of_day}</div>
        )}
        {attraction.altitude && (
          <div className="text-sm text-[var(--text-secondary)]">🏔️ {attraction.altitude}m</div>
        )}
        {attraction.duration_hours && (
          <div className="text-sm text-[var(--text-secondary)]">⏱️ 建议游玩 {attraction.duration_hours}h</div>
        )}
      </div>
      {attraction.highlights && attraction.highlights.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {attraction.highlights.map((h, i) => (
            <span key={i} className="px-2 py-1 bg-[var(--canvas)] text-[var(--accent)] rounded-lg text-xs">{h}</span>
          ))}
        </div>
      )}
      {attraction.tips && <p className="text-sm text-[var(--text-secondary)]">{attraction.tips}</p>}
      {notes && notes.length > 0 && (
        <button
          onClick={onViewPhotos}
          className="w-full py-2.5 border border-[var(--accent)] text-[var(--accent)] rounded-xl text-sm font-medium hover:bg-[var(--accent)] hover:text-white transition"
        >
          📸 查看 {notes.length} 条小红书/抖音笔记
        </button>
      )}
    </div>
  )
}

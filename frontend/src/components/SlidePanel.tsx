import type { Spot } from '../types'

interface SlidePanelProps {
  spot: Spot | null
  onClose: () => void
  children?: React.ReactNode
}

export default function SlidePanel({ spot, onClose, children }: SlidePanelProps) {
  if (!spot) return null

  return (
    <div className="fixed inset-0 z-40">
      <div className="absolute inset-0 bg-black/20" onClick={onClose} />
      <div className="absolute right-0 top-0 h-full w-full max-w-[45%] max-sm:max-w-full bg-[var(--card)] shadow-2xl overflow-auto animate-slide-in">
        <div className="sticky top-0 bg-[var(--card)] p-4 border-b border-[var(--border)] flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-[var(--text-primary)]">{spot.name}</h3>
            <span className="text-xs text-[var(--accent)] uppercase">{spot.category}</span>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-[var(--canvas)] rounded-lg transition">
            ✕
          </button>
        </div>
        <div className="p-4">{children}</div>
      </div>
    </div>
  )
}

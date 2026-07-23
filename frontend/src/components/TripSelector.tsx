import { useState, useEffect } from 'react'
import api from '../services/api'
import type { Trip } from '../types'
import { CaretDown } from '@phosphor-icons/react'

interface TripSelectorProps {
  onSelect: (tripId: number) => void
  selectedId?: number | null
}

export default function TripSelector({ onSelect, selectedId }: TripSelectorProps) {
  const [trips, setTrips] = useState<Trip[]>([])
  const [open, setOpen] = useState(false)

  useEffect(() => {
    api.get('/trips').then(res => setTrips(res.data))
  }, [])

  const selected = trips.find(t => t.id === selectedId)

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-4 py-2 bg-[var(--card)] border border-[var(--border)] rounded-xl text-[var(--text-primary)] text-sm hover:border-[var(--accent)] transition"
      >
        {selected ? selected.name : '选择旅行计划'}
        <CaretDown size={14} className={open ? 'rotate-180 transition' : 'transition'} />
      </button>
      {open && (
        <div className="absolute top-full left-0 mt-1 w-56 bg-[var(--card)] border border-[var(--border)] rounded-xl shadow-lg z-50">
          {trips.map(trip => (
            <button
              key={trip.id}
              onClick={() => { onSelect(trip.id); setOpen(false) }}
              className="w-full text-left px-4 py-2.5 text-sm text-[var(--text-primary)] hover:bg-[var(--canvas)] first:rounded-t-xl last:rounded-b-xl"
            >
              {trip.name}
            </button>
          ))}
          {trips.length === 0 && (
            <div className="px-4 py-3 text-sm text-[var(--text-secondary)]">暂无旅行计划</div>
          )}
        </div>
      )}
    </div>
  )
}

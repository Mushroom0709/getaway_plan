import type { Hotel } from '../types'

interface HotelDetailProps {
  hotel: Hotel
}

export default function HotelDetail({ hotel }: HotelDetailProps) {
  return (
    <div className="space-y-4">
      {hotel.cover_image && (
        <img src={hotel.cover_image} alt={hotel.name} className="w-full h-48 object-cover rounded-xl" />
      )}
      <div>
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">{hotel.name}</h3>
        {hotel.brand && <p className="text-sm text-[var(--text-accent)]">{hotel.brand}</p>}
      </div>
      <div className="grid grid-cols-2 gap-2 text-sm">
        {hotel.rating && <div className="text-[var(--text-secondary)]">⭐ {hotel.rating}</div>}
        {hotel.price_per_room && <div className="text-[var(--text-secondary)]">¥{hotel.price_per_room}/晚</div>}
        {hotel.room_type && <div className="text-[var(--text-secondary)]">{hotel.room_type}</div>}
        {hotel.opened_year && <div className="text-[var(--text-secondary)]">{hotel.opened_year}年开业</div>}
      </div>
      {hotel.features && hotel.features.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {hotel.features.map((f, i) => (
            <span key={i} className="px-2 py-1 bg-[var(--canvas)] text-[var(--text-secondary)] rounded-lg text-xs">{f}</span>
          ))}
        </div>
      )}
      {hotel.phone && <p className="text-sm text-[var(--text-secondary)]">📞 {hotel.phone}</p>}
      {hotel.notes && <p className="text-sm text-[var(--text-secondary)]">{hotel.notes}</p>}
    </div>
  )
}

import { useState, useEffect } from 'react'
import AuthGuard from './components/AuthGuard'
import TripSelector from './components/TripSelector'
import TopNav from './components/TopNav'
import MapPanel from './components/MapPanel'
import SlidePanel from './components/SlidePanel'
import HotelDetail from './components/HotelDetail'
import RestaurantDetail from './components/RestaurantDetail'
import AttractionDetail from './components/AttractionDetail'
import PhotoGallery from './components/PhotoGallery'
import Lightbox from './components/Lightbox'
import Overview from './components/Overview'
import { useTrip } from './hooks/useTrip'
import api from './services/api'
import type { Spot, SocialNote, Trip, Attraction } from './types'
import { NavigationArrow } from '@phosphor-icons/react'

interface SpotImage {
  url: string
  url_large: string
  local_path: string
  author: string
  platform: string
  note_title: string
}

export default function App() {
  const [tripId, setTripId] = useState<number | null>(null)
  const [trips, setTrips] = useState<Trip[]>([])
  const [authVersion, setAuthVersion] = useState(0) // triggers remount on login
  const [activeDay, setActiveDay] = useState('all')
  const [selectedSpot, setSelectedSpot] = useState<Spot | null>(null)
  const [showGallery, setShowGallery] = useState(false)
  const [spotNotes, setSpotNotes] = useState<SocialNote[]>([])
  const [spotImages, setSpotImages] = useState<SpotImage[]>([])
  const [expandedNotes, setExpandedNotes] = useState<Set<number>>(new Set())
  const [noteImages, setNoteImages] = useState<Map<number, SpotImage[]>>(new Map())
  const [lightboxIndex, setLightboxIndex] = useState(0)
  const [showLightbox, setShowLightbox] = useState(false)
  const [spotAttraction, setSpotAttraction] = useState<Attraction | null>(null)

  const { trip, days, spots, hotels, restaurants, attractions, notes, routes, budget, weather } = useTrip(tripId)

  // Auto-select latest trip on mount (only runs when authenticated)
  useEffect(() => {
    if (tripId) return
    if (!localStorage.getItem('token')) return
    api.get('/trips').then(res => {
      const list: Trip[] = res.data || []
      setTrips(list)
      if (list.length > 0) {
        const latest = list.reduce((a, b) => (a.id > b.id ? a : b))
        setTripId(latest.id)
      }
    }).catch(() => { })
  }, [tripId, authVersion])

  const handleSpotClick = async (spot: Spot) => {
    setSelectedSpot(spot)
    setShowGallery(false)
    setSpotNotes([])
    setSpotImages([])
    setExpandedNotes(new Set())
    setNoteImages(new Map())
    setSpotAttraction(null)

    // Load notes
    try {
      const res = await api.get(`/spots/${spot.id}/notes`)
      setSpotNotes(res.data || [])
    } catch { setSpotNotes([]) }

    // Load attraction for scenic/photo spots
    if (spot.category === 'scenic' || spot.category === 'photo') {
      try {
        const res = await api.get(`/spots/${spot.id}/attractions`)
        const list = res.data || []
        if (list.length > 0) setSpotAttraction(list[0])
      } catch { setSpotAttraction(null) }
    }
  }

  const toggleNote = async (noteId: number) => {
    setExpandedNotes(prev => {
      const next = new Set(prev)
      if (next.has(noteId)) {
        next.delete(noteId)
      } else {
        next.add(noteId)
      }
      return next
    })

    // Load images if not already loaded
    if (!noteImages.has(noteId)) {
      try {
        const imgRes = await api.get(`/notes/${noteId}/images`)
        const imgs: SpotImage[] = (imgRes.data || []).map((img: any) => ({
          url: img.url || '',
          url_large: img.url_large || img.local_path || img.url || '',
          local_path: img.local_path || img.url || '',
          author: '',
          platform: '',
          note_title: '',
        }))
        setNoteImages(prev => new Map(prev).set(noteId, imgs))
      } catch { /* ignore */ }
    }
  }

  const handleClosePanel = () => { setSelectedSpot(null); setShowGallery(false); setSpotNotes([]); setSpotImages([]); setExpandedNotes(new Set()); setNoteImages(new Map()) }

  const activeDayNum = activeDay === 'budget' ? -1 : activeDay === 'all' ? -1 : parseInt(activeDay.replace('D', ''))
  const currentDay = days.find(d => d.day_number === activeDayNum)

  const slideContent = () => {
    if (!selectedSpot) return null

    switch (selectedSpot.category) {
      case 'hotel': {
        const hotel = hotels.find(h => h.name === selectedSpot.name)
        const dayForHotel = days.find(d => d.id === selectedSpot.day_id)
        return hotel ? (
          <div>
            <HotelDetail hotel={hotel} />
            {dayForHotel && (
              <div className="mt-4 p-4 bg-[var(--canvas)] rounded-xl">
                <h4 className="font-medium text-sm mb-2">📅 {dayForHotel.title}</h4>
                <p className="text-xs text-[var(--text-secondary)]">
                  住宿城市：{dayForHotel.hotel_city || '—'} · 驾驶约 {dayForHotel.drive_hours || 0}h
                </p>
              </div>
            )}
          </div>
        ) : null
      }
      case 'restaurant': {
        const restaurant = restaurants.find(r => r.name === selectedSpot.name)
        const dayForRest = days.find(d => d.id === selectedSpot.day_id)
        return restaurant ? (
          <div>
            <RestaurantDetail restaurant={restaurant} />
            {dayForRest && (
              <div className="mt-4 p-4 bg-[var(--canvas)] rounded-xl">
                <h4 className="font-medium text-sm mb-2">🍽️ {dayForRest.title}</h4>
                <p className="text-xs text-[var(--text-secondary)]">该天更多美食信息</p>
              </div>
            )}
          </div>
        ) : null
      }
      case 'scenic':
      case 'photo': {
        if (showGallery) {
          return <PhotoGallery notes={spotNotes} />
        }
        const attraction = attractions.find(a => a.spot_id === selectedSpot.id)
        const dayForSpot = days.find(d => d.id === selectedSpot.day_id)

        const navUrl = `https://uri.amap.com/navigation?to=${selectedSpot.lng},${selectedSpot.lat},${encodeURIComponent(selectedSpot.name)}&mode=car&coordinate=gaode`

        return (
          <div>
            {/* Navigate Button */}
            <a
              href={navUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 w-full px-4 py-2.5 mb-4 bg-[var(--accent)] text-white rounded-xl text-sm font-medium hover:bg-[var(--accent-hover)] transition"
            >
              <NavigationArrow size={18} />
              导航到此 · {selectedSpot.name}
            </a>

            {/* Attraction Info */}
            {spotAttraction ? (
              <div>
                <div className="grid grid-cols-2 gap-2 mb-4">
                  {spotAttraction.ticket_price && (
                    <div className="bg-[var(--canvas)] rounded-lg p-2.5">
                      <div className="text-[10px] text-[var(--text-secondary)]">🎫 门票</div>
                      <div className="text-sm font-medium">{spotAttraction.ticket_price}</div>
                    </div>
                  )}
                  {spotAttraction.duration_hours && (
                    <div className="bg-[var(--canvas)] rounded-lg p-2.5">
                      <div className="text-[10px] text-[var(--text-secondary)]">⏱️ 建议时长</div>
                      <div className="text-sm font-medium">{spotAttraction.duration_hours}h</div>
                    </div>
                  )}
                  {spotAttraction.altitude && (
                    <div className="bg-[var(--canvas)] rounded-lg p-2.5">
                      <div className="text-[10px] text-[var(--text-secondary)]">🏔️ 海拔</div>
                      <div className="text-sm font-medium">{spotAttraction.altitude}m</div>
                    </div>
                  )}
                  {spotAttraction.best_time_of_day && (
                    <div className="bg-[var(--canvas)] rounded-lg p-2.5">
                      <div className="text-[10px] text-[var(--text-secondary)]">📸 最佳时间</div>
                      <div className="text-sm font-medium">{spotAttraction.best_time_of_day}</div>
                    </div>
                  )}
                </div>
                {spotAttraction.tips && (
                  <p className="text-xs text-[var(--text-secondary)] mb-3">💡 {spotAttraction.tips}</p>
                )}
                {spotAttraction.highlights && spotAttraction.highlights.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {spotAttraction.highlights.map((h: string, i: number) => (
                      <span key={i} className="px-2 py-0.5 bg-[var(--canvas)] text-[var(--accent)] rounded-md text-xs">{h}</span>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="text-sm text-[var(--text-secondary)] mb-4">{selectedSpot.intro || selectedSpot.description}</div>
            )}

            {/* Photo / Social Notes - collapsible per note */}
            {spotNotes.length > 0 && (
              <div className="mt-4">
                <h4 className="font-medium text-sm mb-3">📸 实拍笔记 ({spotNotes.length}篇)</h4>
                <div className="space-y-1">
                  {spotNotes.map(note => {
                    const isExpanded = expandedNotes.has(note.id)
                    const imgs = noteImages.get(note.id) || []

                    return (
                      <div key={note.id} className="border border-[var(--border)] rounded-lg overflow-hidden">
                        {/* Note header - click to expand */}
                        <button
                          onClick={() => toggleNote(note.id)}
                          className="w-full flex items-center gap-2 px-3 py-2 text-left hover:bg-[var(--canvas)] transition"
                        >
                          <span className="text-sm">{note.platform === 'douyin' ? '🎵' : '📕'}</span>
                          <span className="flex-1 text-xs text-[var(--text-primary)] truncate">
                            {note.title || '无标题'}
                          </span>
                          <span className="text-[10px] text-[var(--text-secondary)] shrink-0">@{note.author}</span>
                          <span className="text-[var(--text-secondary)] text-xs">{isExpanded ? '▾' : '▸'}</span>
                        </button>

                        {/* Expanded images */}
                        {isExpanded && (
                          <div className="px-3 pb-3">
                            {imgs.length > 0 ? (
                              <div className="flex gap-2 overflow-x-auto pb-1">
                                {imgs.map((img, idx) => (
                                  <div
                                    key={idx}
                                    onClick={() => {
                                      // Build flat image list for lightbox
                                      const allImgs: SpotImage[] = []
                                      let targetIdx = 0
                                      spotNotes.forEach(n => {
                                        const nImgs = noteImages.get(n.id) || []
                                        nImgs.forEach(ni => {
                                          if (n.id === note.id && ni.local_path === img.local_path) {
                                            targetIdx = allImgs.length
                                          }
                                          allImgs.push(ni)
                                        })
                                      })
                                      setSpotImages(allImgs)
                                      setLightboxIndex(targetIdx)
                                      setShowLightbox(true)
                                    }}
                                    className="shrink-0 w-28 h-28 rounded-lg overflow-hidden bg-[var(--canvas)] cursor-pointer hover:opacity-90 transition"
                                  >
                                    <img
                                      src={img.local_path || img.url}
                                      alt=""
                                      className="w-full h-full object-cover"
                                      loading="lazy"
                                      onError={(e) => {
                                        (e.target as HTMLImageElement).style.display = 'none'
                                      }}
                                    />
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <p className="text-xs text-[var(--text-secondary)] py-2">加载中...</p>
                            )}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Day Context */}
            {dayForSpot && (
              <div className="mt-4 p-4 bg-[var(--canvas)] rounded-xl">
                <h4 className="font-medium text-sm mb-2">📍 {dayForSpot.title}</h4>
                <p className="text-xs text-[var(--text-secondary)]">
                  驾驶约 {dayForSpot.drive_hours || 0}h · 宿 {dayForSpot.hotel_city || '—'}
                </p>
              </div>
            )}
          </div>
        )
      }
      case 'airport':
      case 'highspeed_rail':
      case 'train':
        return (
          <div>
            <p className="text-sm text-[var(--text-secondary)]">{selectedSpot.intro || selectedSpot.description}</p>
          </div>
        )
      default: {
        // stay / other - show day summary
        const dayForStay = days.find(d => d.id === selectedSpot.day_id)
        const cityHotels = hotels.filter(h => h.city.toLowerCase() === (dayForStay?.hotel_city || '').toLowerCase())
        return (
          <div>
            <p className="text-sm text-[var(--text-secondary)] mb-4">{selectedSpot.intro || selectedSpot.description}</p>
            {dayForStay && (
              <div className="p-4 bg-[var(--canvas)] rounded-xl mb-4">
                <h4 className="font-medium text-sm mb-2">📅 {dayForStay.title}</h4>
                <p className="text-xs text-[var(--text-secondary)]">
                  日期：{dayForStay.date || '—'} · 驾驶约 {dayForStay.drive_hours || 0}h
                </p>
                <p className="text-xs text-[var(--text-secondary)]">
                  住宿地：{dayForStay.hotel_city || '—'}
                </p>
              </div>
            )}
            {cityHotels.length > 0 && (
              <div>
                <h4 className="font-medium text-sm mb-2">🏨 该城住宿</h4>
                {cityHotels.map(h => (
                  <div key={h.id} className="p-3 bg-[var(--canvas)] rounded-lg mb-2">
                    <span className="text-sm font-medium">{h.name}</span>
                    <span className="text-xs text-[var(--text-secondary)] ml-2">⭐{h.rating} · ¥{h.price_per_room}/晚</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )
      }
    }
  }

  return (
    <AuthGuard onLogin={() => setAuthVersion(v => v + 1)}>
      <div className="h-screen flex flex-col bg-[var(--canvas)]">
        {trip && (
          <div className="bg-[var(--card)] border-b border-[var(--border)] px-4 py-2 flex items-center shrink-0 gap-3">
            <span className="text-sm font-semibold text-[var(--text-primary)]">{trip.name}</span>
            <div className="flex-1" />
            <TripSelector onSelect={setTripId} selectedId={tripId} />
          </div>
        )}
        {tripId && !trip ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="animate-spin w-8 h-8 border-2 border-[var(--accent)] border-t-transparent rounded-full" />
          </div>
        ) : trip ? (
          <div className="flex-1 flex">
            {/* Left Sidebar - always visible */}
            <div className="w-44 max-sm:w-32 shrink-0 bg-[var(--card)] border-r border-[var(--border)] overflow-y-auto">
              <TopNav days={days} activeDay={activeDay} onChange={setActiveDay} />
            </div>
            {/* Content area */}
            {activeDay === 'overview' ? (
              <div className="flex-1 overflow-auto p-6">
                <div className="max-w-3xl mx-auto">
                  <Overview days={days} routes={routes} budget={budget} weather={weather} />
                </div>
              </div>
            ) : (
              <div className="flex-1 relative">
                <MapPanel spots={spots} routes={routes} days={days} activeDay={activeDay} onSpotClick={handleSpotClick} />
              </div>
            )}
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-[var(--text-secondary)] text-sm gap-4">
            <div className="bg-white/90 backdrop-blur-sm rounded-xl px-3 py-2 shadow-sm">
              <TripSelector onSelect={setTripId} selectedId={tripId} />
            </div>
            <p>选择或创建一个旅行计划开始规划</p>
          </div>
        )}

        {/* Slide Panel */}
        <SlidePanel spot={selectedSpot} onClose={handleClosePanel}>
          {slideContent()}
        </SlidePanel>

        {/* Lightbox */}
        {showLightbox && spotImages.length > 0 && (
          <Lightbox
            images={spotImages}
            initialIndex={lightboxIndex}
            onClose={() => setShowLightbox(false)}
          />
        )}
      </div>
    </AuthGuard>
  )
}
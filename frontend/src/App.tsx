import { useState } from 'react'
import AuthGuard from './components/AuthGuard'
import TripSelector from './components/TripSelector'
import TopNav from './components/TopNav'
import MainLayout from './components/MainLayout'
import MapPanel from './components/MapPanel'
import DayContent from './components/DayContent'
import SlidePanel from './components/SlidePanel'
import HotelDetail from './components/HotelDetail'
import RestaurantDetail from './components/RestaurantDetail'
import AttractionDetail from './components/AttractionDetail'
import PhotoGallery from './components/PhotoGallery'
import BudgetSummary from './components/BudgetSummary'
import { useTrip } from './hooks/useTrip'
import type { Spot } from './types'

export default function App() {
  const [tripId, setTripId] = useState<number | null>(null)
  const [activeDay, setActiveDay] = useState('D0')
  const [selectedSpot, setSelectedSpot] = useState<Spot | null>(null)
  const [showGallery, setShowGallery] = useState(false)

  const { trip, days, spots, hotels, restaurants, attractions, notes, routes, budget, weather } = useTrip(tripId)

  const handleSpotClick = (spot: Spot) => setSelectedSpot(spot)
  const handleClosePanel = () => { setSelectedSpot(null); setShowGallery(false) }

  const activeDayNum = activeDay === 'budget' ? -1 : parseInt(activeDay.replace('D', ''))
  const currentDay = days.find(d => d.day_number === activeDayNum)

  const slideContent = () => {
    if (!selectedSpot) return null

    switch (selectedSpot.category) {
      case 'hotel': {
        const hotel = hotels.find(h => h.name === selectedSpot.name)
        return hotel ? <HotelDetail hotel={hotel} /> : null
      }
      case 'restaurant': {
        const restaurant = restaurants.find(r => r.name === selectedSpot.name)
        return restaurant ? <RestaurantDetail restaurant={restaurant} /> : null
      }
      case 'scenic':
      case 'photo': {
        if (showGallery) {
          const spotNotes = notes.filter(n => n.spot_id === (attractions.find(a => a.spot_id === selectedSpot.id)?.spot_id))
          return <PhotoGallery notes={notes} />
        }
        const attraction = attractions.find(a => a.spot_id === selectedSpot.id)
        const spotNotes = notes.filter(n => n.spot_id === selectedSpot.id)
        return attraction ? (
          <AttractionDetail
            attraction={attraction}
            notes={spotNotes}
            onViewPhotos={() => setShowGallery(true)}
          />
        ) : (
          <div className="text-sm text-[var(--text-secondary)]">{selectedSpot.intro || selectedSpot.description}</div>
        )
      }
      default:
        return <div className="text-sm text-[var(--text-secondary)]">{selectedSpot.intro || selectedSpot.description}</div>
    }
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-[var(--canvas)]">
        <div className="bg-[var(--card)] border-b border-[var(--border)] px-4 py-3 flex items-center gap-4 max-sm:flex-col max-sm:items-start max-sm:gap-2">
          <TripSelector onSelect={setTripId} selectedId={tripId} />
          {tripId && days.length > 0 && (
            <TopNav days={days} activeDay={activeDay} onChange={setActiveDay} />
          )}
        </div>

        {tripId && !trip ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin w-8 h-8 border-2 border-[var(--accent)] border-t-transparent rounded-full" />
          </div>
        ) : trip ? (
          activeDay === 'budget' ? (
            <div className="max-w-2xl mx-auto p-6">
              <BudgetSummary items={budget} />
            </div>
          ) : (
            <MainLayout
              mapPanel={
                <MapPanel spots={spots} routes={routes} activeDay={activeDay} onSpotClick={handleSpotClick} />
              }
              contentPanel={
                currentDay ? <DayContent day={currentDay} weather={weather.find(w => w.city === currentDay.hotel_city)} /> : null
              }
              slidePanel={
                <SlidePanel spot={selectedSpot} onClose={handleClosePanel}>
                  {slideContent()}
                </SlidePanel>
              }
            />
          )
        ) : (
          <div className="flex items-center justify-center h-64 text-[var(--text-secondary)] text-sm">
            选择或创建一个旅行计划开始规划
          </div>
        )}
      </div>
    </AuthGuard>
  )
}
import { useEffect, useRef } from 'react'
import type { Spot, RouteSegment } from '../types'

declare global {
  interface Window {
    AMap: any
    _onAmapLoad?: () => void
  }
}

interface MapPanelProps {
  spots: Spot[]
  routes: RouteSegment[]
  activeDay: string
  onSpotClick: (spot: Spot) => void
}

const categoryIcons: Record<string, string> = {
  scenic: '⭐',
  photo: '📸',
  hotel: '🏠',
  restaurant: '🍴',
  airport: '✈',
  highspeed_rail: '🚄',
  train: '🚂',
  other: '●',
}

export default function MapPanel({ spots, routes, activeDay, onSpotClick }: MapPanelProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<any>(null)
  const markersRef = useRef<any[]>([])
  const polylinesRef = useRef<any[]>([])

  // Load AMap SDK
  useEffect(() => {
    if (window.AMap) return
    const script = document.createElement('script')
    script.src = 'https://webapi.amap.com/maps?v=2.0&key=f2a8c18781eefe2b345d24ca91418e96'
    script.onload = () => {
      if (window._onAmapLoad) window._onAmapLoad()
    }
    document.head.appendChild(script)
  }, [])

  // Init map
  useEffect(() => {
    const init = () => {
      if (!containerRef.current || !window.AMap) return
      const map = new window.AMap.Map(containerRef.current, {
        zoom: 10,
        center: [101.8, 37.3],
        mapStyle: 'amap://styles/light',
      })
      mapRef.current = map
    }

    if (window.AMap) {
      init()
    } else {
      window._onAmapLoad = init
    }

    return () => {
      if (mapRef.current) mapRef.current.destroy()
    }
  }, [])

  // Update markers
  useEffect(() => {
    if (!mapRef.current || !window.AMap) return

    // Clear old
    markersRef.current.forEach(m => m.remove())
    markersRef.current = []
    polylinesRef.current.forEach(p => p.remove())
    polylinesRef.current = []

    const num = activeDay === 'budget' ? -1 : parseInt(activeDay.replace('D', ''))
    const daySpots = num >= 0 ? spots.filter(s => s.day_id === num) : spots

    daySpots.forEach(spot => {
      const content = `<div style="background:var(--card);border-radius:8px;padding:4px 8px;font-size:12px;white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,0.1);cursor:pointer">${categoryIcons[spot.category] || '●'} ${spot.name}</div>`
      const marker = new window.AMap.Marker({
        position: [spot.lng, spot.lat],
        content,
        offset: new window.AMap.Pixel(0, -20),
      })
      marker.on('click', () => onSpotClick(spot))
      mapRef.current.add(marker)
      markersRef.current.push(marker)
    })

    // Routes
    const dayRoutes = num >= 0 ? routes.filter(r => r.day_number === num) : []
    dayRoutes.forEach(route => {
      if (!route.polyline) return
      const path = route.polyline.split(';').map(p => {
        const [lng, lat] = p.split(',').map(Number)
        return [lng, lat]
      })
      const polyline = new window.AMap.Polyline({
        path,
        strokeColor: route.color || '#4caf50',
        strokeWeight: 5,
        strokeOpacity: 0.8,
        showDir: true,
      })
      mapRef.current.add(polyline)
      polylinesRef.current.push(polyline)
    })

    if (daySpots.length > 0) {
      mapRef.current.setFitView()
    }
  }, [spots, routes, activeDay, onSpotClick])

  return <div ref={containerRef} className="w-full h-full" />
}

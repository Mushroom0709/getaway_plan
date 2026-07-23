import { useEffect, useRef, useState } from 'react'
import type { Spot, RouteSegment, Day } from '../types'

declare global {
  interface Window {
    AMap: any
    _onAmapLoad?: () => void
  }
}

interface MapPanelProps {
  spots: Spot[]
  routes: RouteSegment[]
  days: Day[]
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

const dayColors: Record<number, string> = {
  0: '#4caf50',
  1: '#2196f3',
  2: '#ff9800',
  3: '#e91e63',
  4: '#9c27b0',
  5: '#00bcd4',
  6: '#ff5722',
}

export default function MapPanel({ spots, routes, days, activeDay, onSpotClick }: MapPanelProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<any>(null)
  const markersRef = useRef<any[]>([])
  const polylinesRef = useRef<any[]>([])
  const [mapReady, setMapReady] = useState(false)

  useEffect(() => {
    if (window.AMap) return
    const script = document.createElement('script')
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${import.meta.env.VITE_AMAP_KEY || 'your_amap_key'}`
    script.onload = () => window._onAmapLoad?.()
    document.head.appendChild(script)
  }, [])

  useEffect(() => {
    const init = () => {
      if (!containerRef.current || !window.AMap) return
      const map = new window.AMap.Map(containerRef.current, {
        zoom: 7,
        center: [100.5, 39.0],
        mapStyle: 'amap://styles/light',
      })
      mapRef.current = map
      setMapReady(true)
    }

    if (window.AMap) { init() }
    else { window._onAmapLoad = init }

    return () => { mapRef.current?.destroy() }
  }, [])

  // Render ALL spots and ALL routes, with activeDay emphasis
  useEffect(() => {
    if (!mapRef.current || !window.AMap) return

    markersRef.current.forEach(m => m.remove())
    markersRef.current = []
    polylinesRef.current.forEach(p => p.remove())
    polylinesRef.current = []

    const activeNum = activeDay === 'budget' || activeDay === 'all' ? -1 : parseInt(activeDay.replace('D', ''))

    // Build day_number <-> day_id mappings
    const dayNumToId = new Map<number, number>()
    const dayIdToNum = new Map<number, number>()
    days.forEach(d => {
      dayNumToId.set(d.day_number, d.id)
      dayIdToNum.set(d.id, d.day_number)
    })
    const activeDayId = activeNum >= 0 ? dayNumToId.get(activeNum) : undefined

    // ---- ALL spots ----
    spots.forEach(spot => {
      const spotDayNum = spot.day_id ? dayIdToNum.get(spot.day_id) : undefined
      const isActive = activeNum < 0 || spot.day_id === activeDayId
      const opacity = isActive ? '1' : '0.4'
      const icon = categoryIcons[spot.category] || '●'
      const borderColor = dayColors[spotDayNum ?? 0] || '#999'
      const content = `<div style="background:#fff;border-radius:6px;padding:2px 6px;font-size:11px;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,0.15);cursor:pointer;opacity:${opacity};border-left:3px solid ${borderColor}">${icon} ${spot.name}</div>`
      const marker = new window.AMap.Marker({
        position: [spot.lng, spot.lat],
        content,
        offset: new window.AMap.Pixel(0, -16),
        zIndex: isActive ? 100 : 50,
      })
      marker.on('click', () => onSpotClick(spot))
      mapRef.current.add(marker)
      markersRef.current.push(marker)
    })

    // ---- ALL routes ----
    // Group routes by day_number, deduplicate overlapping segments
    const dayRouteMap = new Map<number, RouteSegment[]>()
    routes.forEach(route => {
      const dn = route.day_number ?? 0
      if (!dayRouteMap.has(dn)) dayRouteMap.set(dn, [])
      dayRouteMap.get(dn)!.push(route)
    })

    dayRouteMap.forEach((dayRoutes, dayNum) => {
      const isActive = activeNum < 0 || dayNum === activeNum
      const color = dayColors[dayNum] || '#999'
      const weight = isActive ? 6 : 3
      const opacity = isActive ? 0.9 : 0.35

      dayRoutes.forEach(route => {
        if (!route.polyline) return
        const path = route.polyline.split(';').map(p => {
          const [lng, lat] = p.split(',').map(Number)
          return [lng, lat]
        })
        const isTransit = route.route_type === 'transit'
        const polyline = new window.AMap.Polyline({
          path,
          strokeColor: color,
          strokeWeight: weight,
          strokeOpacity: opacity,
          strokeStyle: isTransit ? 'dashed' : 'solid',
          strokeDasharray: isTransit ? [10, 8] : undefined,
          showDir: !isTransit && isActive,
          zIndex: isActive ? 80 : 30,
        })
        mapRef.current.add(polyline)
        polylinesRef.current.push(polyline)
      })
    })

    // Fit view: per-day tight fit (spots + route polylines), or all-main-area
    const lngs: number[] = []
    const lats: number[] = []

    if (activeDayId) {
      // Include spots for this day
      spots.filter(s => s.day_id === activeDayId).forEach(s => {
        lngs.push(s.lng)
        lats.push(s.lat)
      })
      // Include route polyline points for this day
      routes.filter(r => r.day_number === activeNum).forEach(r => {
        if (!r.polyline) return
        r.polyline.split(';').forEach(p => {
          const [lng, lat] = p.split(',').map(Number)
          if (!isNaN(lng) && !isNaN(lat)) {
            lngs.push(lng)
            lats.push(lat)
          }
        })
      })
    } else {
      spots.filter(s => s.lng < 110 && s.lat > 35).forEach(s => {
        lngs.push(s.lng)
        lats.push(s.lat)
      })
    }

    if (lngs.length > 0) {
      const sw = new window.AMap.LngLat(Math.min(...lngs), Math.min(...lats))
      const ne = new window.AMap.LngLat(Math.max(...lngs), Math.max(...lats))
      mapRef.current.setBounds(new window.AMap.Bounds(sw, ne), false, [50, 50, 50, 50])
    }
  }, [spots, routes, activeDay, onSpotClick, mapReady])

  return <div ref={containerRef} className="w-full h-full" />
}

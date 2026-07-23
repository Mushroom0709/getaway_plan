export interface Trip {
  id: number
  name: string
  status: string
  start_date?: string
  end_date?: string
  created_at: string
}

export interface Day {
  id: number
  trip_id: number
  day_number: number
  date?: string
  title?: string
  drive_hours?: number
  hotel_city?: string
  sort_order: number
}

export interface Spot {
  id: number
  trip_id: number
  day_id?: number
  name: string
  lng: number
  lat: number
  category: string
  is_nav_point: boolean
  nav_order?: number
  arrival_time?: string
  description?: string
  intro?: string
}

export interface Hotel {
  id: number
  spot_id?: number
  city: string
  name: string
  brand?: string
  rating?: number
  opened_year?: number
  price_per_room?: number
  room_type?: string
  features?: string[]
  lng?: number
  lat?: number
  phone?: string
  cover_image?: string
  notes?: string
}

export interface Restaurant {
  id: number
  spot_id?: number
  city: string
  name: string
  address?: string
  rating?: number
  avg_price?: number
  cuisine?: string
  cover_image?: string
  dishes?: Dish[]
}

export interface Dish {
  id: number
  name: string
  price?: number
  is_signature: boolean
}

export interface Attraction {
  id: number
  spot_id: number
  ticket_price?: string
  opening_hours?: string
  best_time_of_day?: string
  duration_hours?: number
  altitude?: number
  tips?: string
  highlights?: string[]
  must_see: boolean
}

export interface SocialNote {
  id: number
  spot_id?: number
  platform: string
  title?: string
  author?: string
  likes: number
  description?: string
  images: SocialImage[]
}

export interface SocialImage {
  id: number
  url?: string
  url_large?: string
  width?: number
  height?: number
  sort_order: number
}

export interface RouteSegment {
  id: number
  from_spot_id?: number
  to_spot_id?: number
  distance_km?: number
  duration_min?: number
  polyline?: string
  color?: string
  day_number?: number
  route_type?: string  // "driving" or "transit"
}

export interface BudgetItem {
  id: number
  category: string
  item: string
  unit_price?: number
  quantity: number
  subtotal?: number
}

export interface Weather {
  id: number
  city: string
  date: string
  high_temp?: string
  low_temp?: string
  weather_desc?: string
  advice?: string
}

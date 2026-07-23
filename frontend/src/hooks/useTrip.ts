import { useState, useEffect } from 'react'
import api from '../services/api'
import type { Trip, Day, Spot, Hotel, Restaurant, Attraction, SocialNote, RouteSegment, BudgetItem, Weather } from '../types'

interface TripData {
  trip: Trip | null
  days: Day[]
  spots: Spot[]
  hotels: Hotel[]
  restaurants: Restaurant[]
  attractions: Attraction[]
  notes: SocialNote[]
  routes: RouteSegment[]
  budget: BudgetItem[]
  weather: Weather[]
  isLoading: boolean
  error: string | null
}

export function useTrip(tripId: number | null): TripData {
  const [data, setData] = useState<TripData>({
    trip: null, days: [], spots: [], hotels: [], restaurants: [],
    attractions: [], notes: [], routes: [], budget: [], weather: [],
    isLoading: true, error: null
  })

  useEffect(() => {
    if (!tripId) { setData(d => ({ ...d, isLoading: false })); return }
    setData(d => ({ ...d, isLoading: true }))
    Promise.all([
      api.get(`/trips/${tripId}`),
      api.get(`/trips/${tripId}/spots`),
      api.get(`/trips/${tripId}/hotels`),
      api.get(`/trips/${tripId}/restaurants`),
      api.get(`/trips/${tripId}/routes`),
      api.get(`/trips/${tripId}/budget_items`),
      api.get(`/trips/${tripId}/weathers`),
    ]).then(([tripRes, spotsRes, hotelsRes, restRes, routesRes, budgetRes, weatherRes]) => {
      setData({
        trip: tripRes.data, days: tripRes.data.days || [],
        spots: spotsRes.data, hotels: hotelsRes.data,
        restaurants: restRes.data, attractions: [],
        notes: [], routes: routesRes.data,
        budget: budgetRes.data, weather: weatherRes.data,
        isLoading: false, error: null
      })
    }).catch(err => {
      setData(d => ({ ...d, isLoading: false, error: err.message }))
    })
  }, [tripId])

  return data
}

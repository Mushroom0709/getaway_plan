import { useState, useEffect } from 'react'
import api from '../services/api'

interface AuthState {
  token: string | null
  isLoading: boolean
  login: (password: string) => Promise<void>
  logout: () => void
}

export function useAuth(): AuthState {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const t = localStorage.getItem('token')
    if (t) {
      api.get('/auth/verify').then(() => {
        setToken(t)
        setIsLoading(false)
      }).catch(() => {
        localStorage.removeItem('token')
        setToken(null)
        setIsLoading(false)
      })
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (password: string) => {
    const res = await api.post('/auth/login', { password })
    localStorage.setItem('token', res.data.token)
    setToken(res.data.token)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
  }

  return { token, isLoading, login, logout }
}

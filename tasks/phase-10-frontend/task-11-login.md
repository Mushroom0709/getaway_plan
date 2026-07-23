# S11: 前端登录 — LoginPage + AuthGuard + API 层

## Goal

实现前端登录认证：API 服务层（Axios + JWT 拦截器）、LoginPage、AuthGuard、useAuth hook。

## Recipe

### 文件 1: frontend/src/services/api.ts
```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

### 文件 2: frontend/src/hooks/useAuth.ts
```typescript
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
```

### 文件 3: frontend/src/components/LoginPage.tsx
```tsx
import { useState } from 'react'

interface LoginPageProps {
  onLogin: (password: string) => Promise<void>
  error?: string
}

export default function LoginPage({ onLogin, error }: LoginPageProps) {
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await onLogin(password)
    } catch {
      // error handled by parent
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-[var(--canvas)] flex items-center justify-center p-4">
      <div className="bg-[var(--card)] rounded-2xl shadow-[var(--shadow)] p-8 max-w-sm w-full">
        <h1 className="text-2xl font-semibold text-[var(--text-primary)] mb-2">
          Getaway Plan
        </h1>
        <p className="text-[var(--text-secondary)] mb-6 text-sm">
          输入密码以继续
        </p>
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="密码"
            className="w-full px-4 py-3 rounded-xl border border-[var(--border)] bg-[var(--canvas)] text-[var(--text-primary)] placeholder-[var(--text-secondary)] outline-none focus:ring-2 focus:ring-[var(--accent)] transition mb-3"
            autoFocus
          />
          {error && (
            <p className="text-red-500 text-sm mb-3">{error}</p>
          )}
          <button
            type="submit"
            disabled={loading || !password}
            className="w-full py-3 rounded-xl bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white font-medium transition disabled:opacity-50"
          >
            {loading ? '登录中...' : '登录'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### 文件 4: frontend/src/components/AuthGuard.tsx
```tsx
import { useAuth } from '../hooks/useAuth'
import LoginPage from './LoginPage'
import { useState } from 'react'

interface AuthGuardProps {
  children: React.ReactNode
}

export default function AuthGuard({ children }: AuthGuardProps) {
  const { token, isLoading, login } = useAuth()
  const [error, setError] = useState<string>()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[var(--canvas)] flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-[var(--accent)] border-t-transparent rounded-full" />
      </div>
    )
  }

  if (!token) {
    return <LoginPage onLogin={async (p) => {
      try {
        await login(p)
      } catch {
        setError('密码错误，请重试')
      }
    }} error={error} />
  }

  return <>{children}</>
}
```

### 文件 5: frontend/src/App.tsx — 更新
```tsx
import AuthGuard from './components/AuthGuard'

export default function App() {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-[var(--canvas)] flex items-center justify-center">
        <h1 className="text-2xl font-bold text-[var(--text-primary)]">
          Getaway Plan
        </h1>
      </div>
    </AuthGuard>
  )
}
```

## Verification

```bash
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1/frontend
npx tsc --noEmit 2>&1 | grep -v node_modules | head -10
```
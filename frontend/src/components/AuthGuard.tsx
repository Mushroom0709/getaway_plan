import { useAuth } from '../hooks/useAuth'
import LoginPage from './LoginPage'
import { useState } from 'react'

interface AuthGuardProps {
  children: React.ReactNode
  onLogin?: () => void
}

export default function AuthGuard({ children, onLogin }: AuthGuardProps) {
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
      try { await login(p); onLogin?.() } catch { setError('密码错误，请重试') }
    }} error={error} />
  }

  return <>{children}</>
}

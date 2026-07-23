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

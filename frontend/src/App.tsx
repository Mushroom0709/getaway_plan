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

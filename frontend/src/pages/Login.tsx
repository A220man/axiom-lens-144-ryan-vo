import { useAuth } from '../hooks/useAuth'

export function Login() {
  const { login, loading } = useAuth()

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="card w-full max-w-md text-center">
        <h1 className="text-2xl font-bold mb-2">Axiom Lens</h1>
        <p className="text-[var(--color-text-muted)] mb-6">Android Automation with AI</p>
        <button onClick={login} className="btn-primary w-full" disabled={loading}>
          {loading ? 'Redirecting...' : 'Sign in with Keycloak'}
        </button>
        <p className="text-sm text-[var(--color-text-muted)] mt-4">
          Demo mode: OIDC flow with Keycloak. Tokens stored in memory (sessionStorage).
        </p>
      </div>
    </div>
  )
}

import { useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'


export function Callback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  useEffect(() => {
    async function handleCallback() {
      const code = searchParams.get('code')
      const state = searchParams.get('state')

      if (!code || !state) {
        navigate('/login')
        return
      }

      try {
        await api.get(`/api/v1/auth/callback?code=${code}&state=${state}`)

        // In a real app, decode JWT and get user info
        const user = {
          id: 'demo-user',
          name: 'Demo User',
          email: 'demo@example.com',
          roles: ['operator'],
        }
        sessionStorage.setItem('axiom_lens_user', JSON.stringify(user))
        navigate('/')
      } catch {
        navigate('/login')
      }
    }
    handleCallback()
  }, [searchParams, navigate])

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="card text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-3 border-[var(--color-border)] border-t-[var(--color-primary)] mx-auto mb-4"></div>
        <p className="text-[var(--color-text-muted)]">Completing sign in...</p>
      </div>
    </div>
  )
}

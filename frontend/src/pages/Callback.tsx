import { useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'


export function Callback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { handleCallback } = useAuth()

  useEffect(() => {
    async function handleCallbackWrapper() {
      const code = searchParams.get('code')
      const state = searchParams.get('state')

      if (!code || !state) {
        navigate('/login')
        return
      }

      try {
        await handleCallback(code, state)
        navigate('/')
      } catch {
        navigate('/login')
      }
    }
    handleCallbackWrapper()
  }, [searchParams, navigate, handleCallback])

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="card text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-3 border-[var(--color-border)] border-t-[var(--color-primary)] mx-auto mb-4"></div>
        <p className="text-[var(--color-text-muted)]">Completing sign in...</p>
      </div>
    </div>
  )
}

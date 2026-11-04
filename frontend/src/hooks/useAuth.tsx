import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface User {
  id: string
  name: string
  email: string
  roles: string[]
}

interface TokenData {
  access_token: string
  token_type: string
  expires_in: number
}

interface AuthContextType {
  user: User | null
  token: TokenData | null
  isAuthenticated: boolean
  loading: boolean
  login: () => void
  handleCallback: (code: string, state: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<TokenData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for stored session (in memory for SPA PKCE)
    const storedUser = sessionStorage.getItem('axiom_lens_user')
    const storedToken = sessionStorage.getItem('axiom_lens_token')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    if (storedToken) {
      setToken(JSON.parse(storedToken))
    }
    setLoading(false)
  }, [])

  const login = () => {
    window.location.href = `${API_URL}/api/v1/auth/login`
  }

  const handleCallback = async (code: string, state: string) => {
    const response = await fetch(`${API_URL}/api/v1/auth/callback?code=${code}&state=${state}`)
    if (!response.ok) {
      throw new Error('Authentication failed')
    }
    const tokenData: TokenData = await response.json()
    setToken(tokenData)
    sessionStorage.setItem('axiom_lens_token', JSON.stringify(tokenData))

    // Decode token to get user info (simplified - in production use proper JWT parsing)
    try {
      const payload = JSON.parse(atob(tokenData.access_token.split('.')[1]))
      const userData: User = {
        id: payload.sub,
        name: payload.preferred_username || payload.name || 'Unknown',
        email: payload.email || '',
        roles: payload.realm_access?.roles || [],
      }
      setUser(userData)
      sessionStorage.setItem('axiom_lens_user', JSON.stringify(userData))
    } catch {
      // Fallback user
      const userData: User = {
        id: 'unknown',
        name: 'User',
        email: '',
        roles: [],
      }
      setUser(userData)
      sessionStorage.setItem('axiom_lens_user', JSON.stringify(userData))
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    sessionStorage.removeItem('axiom_lens_user')
    sessionStorage.removeItem('axiom_lens_token')
  }

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!user, loading, login, handleCallback, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

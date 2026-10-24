import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from '../hooks/useAuth'
import { App } from '../App'

const renderApp = () => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  )
}

describe('App', () => {
  it('redirects to login when not authenticated', () => {
    renderApp()
    expect(screen.getByText('Sign in with Keycloak')).toBeInTheDocument()
  })

  it('shows login page initially (auth loads from sessionStorage)', () => {
    sessionStorage.setItem('axiom_lens_user', JSON.stringify({
      id: 'test',
      name: 'Test User',
      email: 'test@example.com',
      roles: ['operator'],
    }))

    renderApp()
    expect(screen.getByText('Axiom Lens')).toBeInTheDocument()
  })
})

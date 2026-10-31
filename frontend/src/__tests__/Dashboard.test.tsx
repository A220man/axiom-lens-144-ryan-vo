import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from '../hooks/useAuth'
import { Dashboard } from '../pages/Dashboard'
import { api } from '../api/client'

vi.mock('../api/client')

const renderDashboard = () => {
  sessionStorage.setItem('axiom_lens_user', JSON.stringify({
    id: 'test',
    name: 'Test User',
    email: 'test@example.com',
    roles: ['operator'],
  }))

  return render(
    <BrowserRouter>
      <AuthProvider>
        <Dashboard />
      </AuthProvider>
    </BrowserRouter>
  )
}

describe('Dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.setItem('axiom_lens_user', JSON.stringify({
      id: 'test',
      name: 'Test User',
      email: 'test@example.com',
      roles: ['operator'],
    }))
  })

  it('shows loading state initially', () => {
    renderDashboard()
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('displays stats after loading', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: [] })
    vi.mocked(api.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(api.get).mockResolvedValueOnce({ data: [] })

    renderDashboard()

    await waitFor(() => {
      expect(screen.getByText('Total Tasks')).toBeInTheDocument()
      expect(screen.getByText('Active Tasks')).toBeInTheDocument()
      expect(screen.getByText('Connected Devices')).toBeInTheDocument()
    })
  })
})

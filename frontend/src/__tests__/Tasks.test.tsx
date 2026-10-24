import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from '../hooks/useAuth'
import { Tasks } from '../pages/Tasks'

vi.mock('../api/client', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

const renderTasks = () => {
  sessionStorage.setItem('axiom_lens_user', JSON.stringify({
    id: 'test',
    name: 'Test User',
    email: 'test@example.com',
    roles: ['operator'],
  }))

  return render(
    <BrowserRouter>
      <AuthProvider>
        <Tasks />
      </AuthProvider>
    </BrowserRouter>
  )
}

describe('Tasks', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.setItem('axiom_lens_user', JSON.stringify({
      id: 'test',
      name: 'Test User',
      email: 'test@example.com',
      roles: ['operator'],
    }))
  })

  it('shows empty state when no tasks', async () => {
    const { api } = await import('../api/client')
    api.get.mockResolvedValue({ data: [] })

    renderTasks()

    await waitFor(() => {
      expect(screen.getByText(/No tasks yet/i)).toBeInTheDocument()
    })
  })

  it('allows submitting a new task', async () => {
    const { api } = await import('../api/client')
    api.get.mockResolvedValue({ data: [] })
    api.post.mockResolvedValue({})

    renderTasks()

    await waitFor(() => {
      const input = screen.getByPlaceholderText(/Enter automation goal/i)
      fireEvent.change(input, { target: { value: 'Open Settings and enable Dark Theme' } })
      fireEvent.click(screen.getByText('Submit Task'))
    })

    expect(api.post).toHaveBeenCalledWith('/api/v1/tasks', {
      goal: 'Open Settings and enable Dark Theme',
    })
  })
})

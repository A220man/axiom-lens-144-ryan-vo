import { useEffect, useState } from 'react'
import { api } from '../api/client'

interface Task {
  id: string
  goal: string
  device_id: string | null
  model: string | null
  status: string
  created_at: string
  result: any | null
}

export function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [goal, setGoal] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetchTasks()
  }, [])

  async function fetchTasks() {
    try {
      const res = await api.get('/api/v1/tasks')
      setTasks(res.data)
    } catch {
      // Ignore
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!goal.trim()) return
    setSubmitting(true)
    try {
      await api.post('/api/v1/tasks', { goal: goal.trim() })
      setGoal('')
      fetchTasks()
    } catch {
      // Ignore
    } finally {
      setSubmitting(false)
    }
  }

  function getStatusColor(status: string) {
    switch (status) {
      case 'completed': return 'var(--color-success)'
      case 'running': return 'var(--color-warning)'
      case 'failed': return 'var(--color-error)'
      default: return 'var(--color-text-muted)'
    }
  }

  return (
    <div className="card">
      <form onSubmit={handleSubmit} className="mb-6 flex gap-2">
        <input
          type="text"
          value={goal}
          onChange={e => setGoal(e.target.value)}
          placeholder="Enter automation goal (e.g., 'Open Settings and enable Dark Theme')"
          className="flex-1"
          disabled={submitting}
        />
        <button type="submit" className="btn-primary" disabled={submitting || !goal.trim()}>
          {submitting ? 'Submitting...' : 'Submit Task'}
        </button>
      </form>

      {loading ? (
        <div className="text-center text-[var(--color-text-muted)]">Loading tasks...</div>
      ) : tasks.length === 0 ? (
        <div className="text-center text-[var(--color-text-muted)] py-8">No tasks yet. Submit your first automation goal above.</div>
      ) : (
        <div className="space-y-3">
          {tasks.map(task => (
            <div key={task.id} className="flex items-center justify-between p-4 bg-[var(--color-bg)] rounded border border-[var(--color-border)]">
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">{task.goal}</p>
                <p className="text-sm text-[var(--color-text-muted)]">
                  {task.device_id ? `Device: ${task.device_id}` : 'No device'} •
                  {task.model ? ` Model: ${task.model}` : ''} •
                  {new Date(task.created_at).toLocaleString()}
                </p>
              </div>
              <span
                className="px-3 py-1 rounded-full text-sm font-medium"
                style={{ backgroundColor: `${getStatusColor(task.status)}22`, color: getStatusColor(task.status) }}
              >
                {task.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

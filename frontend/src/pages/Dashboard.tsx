import { useEffect, useState } from 'react'
import { api } from '../api/client'

interface Stats {
  totalTasks: number
  activeTasks: number
  connectedDevices: number
}

export function Dashboard() {
  const [stats, setStats] = useState<Stats>({ totalTasks: 0, activeTasks: 0, connectedDevices: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchStats() {
      try {
        const [tasksRes, devicesRes] = await Promise.all([
          api.get('/api/v1/tasks'),
          api.get('/api/v1/devices'),
        ])
        const tasks = tasksRes.data
        const devices = devicesRes.data
        setStats({
          totalTasks: tasks.length,
          activeTasks: tasks.filter((t: any) => t.status === 'running').length,
          connectedDevices: devices.filter((d: any) => d.status === 'connected').length,
        })
      } catch {
        // Ignore errors in demo
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
  }, [])

  if (loading) return <div className="flex items-center justify-center h-64">Loading...</div>

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <div className="card">
        <h3 className="text-sm text-[var(--color-text-muted)] mb-2">Total Tasks</h3>
        <p className="text-3xl font-bold">{stats.totalTasks}</p>
      </div>
      <div className="card">
        <h3 className="text-sm text-[var(--color-text-muted)] mb-2">Active Tasks</h3>
        <p className="text-3xl font-bold text-[var(--color-warning)]">{stats.activeTasks}</p>
      </div>
      <div className="card">
        <h3 className="text-sm text-[var(--color-text-muted)] mb-2">Connected Devices</h3>
        <p className="text-3xl font-bold text-[var(--color-success)]">{stats.connectedDevices}</p>
      </div>
    </div>
  )
}

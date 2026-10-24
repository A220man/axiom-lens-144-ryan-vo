import { useEffect, useState } from 'react'
import { api } from '../api/client'

interface Device {
  id: string
  name: string
  platform: string
  status: string
  properties: Record<string, any>
}

export function Devices() {
  const [devices, setDevices] = useState<Device[]>([])
  const [loading, setLoading] = useState(true)
  const [connecting, setConnecting] = useState<string | null>(null)

  useEffect(() => {
    fetchDevices()
  }, [])

  async function fetchDevices() {
    try {
      const res = await api.get('/api/v1/devices')
      setDevices(res.data)
    } catch {
      // Ignore
    } finally {
      setLoading(false)
    }
  }

  async function handleConnect(id: string) {
    setConnecting(id)
    try {
      await api.post(`/api/v1/devices/${id}/connect`)
      fetchDevices()
    } catch {
      // Ignore
    } finally {
      setConnecting(null)
    }
  }

  async function handleDisconnect(id: string) {
    setConnecting(id)
    try {
      await api.post(`/api/v1/devices/${id}/disconnect`)
      fetchDevices()
    } catch {
      // Ignore
    } finally {
      setConnecting(null)
    }
  }

  return (
    <div className="card">
      <h2 className="mb-4">Connected Devices</h2>

      {loading ? (
        <div className="text-center text-[var(--color-text-muted)]">Loading devices...</div>
      ) : devices.length === 0 ? (
        <div className="text-center text-[var(--color-text-muted)] py-8">
          No devices connected. Connect an Android device via ADB or use the WebUSB bridge (planned).
        </div>
      ) : (
        <div className="space-y-3">
          {devices.map(device => (
            <div key={device.id} className="flex items-center justify-between p-4 bg-[var(--color-bg)] rounded border border-[var(--color-border)]">
              <div>
                <p className="font-medium">{device.name}</p>
                <p className="text-sm text-[var(--color-text-muted)]">
                  {device.platform} • {device.id}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className="px-3 py-1 rounded-full text-sm font-medium"
                  style={{
                    backgroundColor: device.status === 'connected'
                      ? 'var(--color-success)22'
                      : 'var(--color-text-muted)22',
                    color: device.status === 'connected' ? 'var(--color-success)' : 'var(--color-text-muted)',
                  }}
                >
                  {device.status}
                </span>
                {device.status === 'connected' ? (
                  <button
                    onClick={() => handleDisconnect(device.id)}
                    disabled={connecting === device.id}
                    className="btn-secondary"
                  >
                    Disconnect
                  </button>
                ) : (
                  <button
                    onClick={() => handleConnect(device.id)}
                    disabled={connecting === device.id}
                    className="btn-primary"
                  >
                    Connect
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

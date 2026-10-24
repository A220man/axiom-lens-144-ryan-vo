import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Tasks } from './pages/Tasks'
import { Devices } from './pages/Devices'
import { Login } from './pages/Login'
import { Callback } from './pages/Callback'
import { useAuth } from './hooks/useAuth'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth()
  if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/callback" element={<Callback />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="tasks" element={<Tasks />} />
        <Route path="devices" element={<Devices />} />
      </Route>
    </Routes>
  )
}

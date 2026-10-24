import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export function Layout() {
  const { user, logout } = useAuth()
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/tasks', label: 'Tasks' },
    { path: '/devices', label: 'Devices' },
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <header className="flex items-center justify-between p-4 border-b border-[var(--color-border)] bg-[var(--color-surface)]">
        <Link to="/" className="font-semibold text-xl">Axiom Lens</Link>
        <nav className="flex items-center gap-4">
          {navItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              className={`px-3 py-2 rounded ${location.pathname === item.path ? 'bg-[var(--color-primary)] text-white' : 'text-[var(--color-text-muted)] hover:text-white'}`}
            >
              {item.label}
            </Link>
          ))}
          {user && (
            <div className="flex items-center gap-3">
              <span className="text-sm text-[var(--color-text-muted)]">{user.name}</span>
              <button onClick={logout} className="btn-secondary">Logout</button>
            </div>
          )}
        </nav>
      </header>
      <main className="flex-1 container py-6">
        <Outlet />
      </main>
      <footer className="border-t border-[var(--color-border)] py-4 px-4 text-center text-sm text-[var(--color-text-muted)]">
        Axiom Lens | Ryan Vo | AI & Machine Learning
      </footer>
    </div>
  )
}

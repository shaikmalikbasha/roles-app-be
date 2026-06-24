import { createFileRoute, redirect, Outlet, Link, useNavigate } from '@tanstack/react-router'
import { LayoutDashboard, Users, Shield, Key, LogOut } from 'lucide-react'
import { isAuthenticated, clearToken } from '@/lib/auth'
import { Button } from '@/components/ui/button'

export const Route = createFileRoute('/_app')({
  beforeLoad: () => {
    if (!isAuthenticated()) throw redirect({ to: '/login' })
  },
  component: AppLayout,
})

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/users', label: 'Users', icon: Users },
  { to: '/roles', label: 'Roles', icon: Shield },
  { to: '/permissions', label: 'Permissions', icon: Key },
] as const

function AppLayout() {
  const navigate = useNavigate()

  function logout() {
    clearToken()
    navigate({ to: '/login' })
  }

  return (
    <div className="flex min-h-screen">
      <aside className="flex w-52 shrink-0 flex-col border-r bg-muted/40">
        <div className="border-b px-4 py-3">
          <span className="font-semibold">Roles App</span>
        </div>
        <nav className="flex flex-1 flex-col gap-1 p-2">
          {navItems.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              activeProps={{ className: 'bg-accent text-accent-foreground font-medium' }}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </nav>
        <div className="border-t p-2">
          <Button variant="ghost" size="sm" className="w-full justify-start gap-2" onClick={logout}>
            <LogOut size={16} />
            Sign out
          </Button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}

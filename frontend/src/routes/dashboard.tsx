import { createFileRoute, redirect, useNavigate } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { clearToken, isAuthenticated } from '@/lib/auth'
import { Button } from '@/components/ui/button'

export const Route = createFileRoute('/dashboard')({
  beforeLoad: () => {
    if (!isAuthenticated()) throw redirect({ to: '/login' })
  },
  component: Dashboard,
})

function Dashboard() {
  const navigate = useNavigate()
  const { data: me, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: api.me,
  })

  function logout() {
    clearToken()
    navigate({ to: '/login' })
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
          <h1 className="text-lg font-semibold">Roles App</h1>
          <Button variant="outline" size="sm" onClick={logout}>
            Sign out
          </Button>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-8">
        {isLoading ? (
          <p className="text-muted-foreground">Loading…</p>
        ) : me ? (
          <div className="space-y-1">
            <p className="text-foreground font-medium">{me.email}</p>
            <p className="text-sm text-muted-foreground">
              Roles: {me.roles.length ? me.roles.join(', ') : 'none'}
            </p>
            <p className="text-sm text-muted-foreground">
              Permissions: {me.permissions.length ? me.permissions.join(', ') : 'none'}
            </p>
          </div>
        ) : null}
      </main>
    </div>
  )
}

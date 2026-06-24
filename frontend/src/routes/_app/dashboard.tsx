import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export const Route = createFileRoute('/_app/dashboard')({
  component: Dashboard,
})

function Dashboard() {
  const { data: me, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: api.me,
  })

  return (
    <div className="px-6 py-8">
      <h2 className="mb-4 text-xl font-semibold">Dashboard</h2>
      {isLoading ? (
        <p className="text-muted-foreground">Loading…</p>
      ) : me ? (
        <div className="space-y-1">
          <p className="font-medium text-foreground">{me.email}</p>
          <p className="text-sm text-muted-foreground">
            Roles: {me.roles.length ? me.roles.join(', ') : 'none'}
          </p>
          <p className="text-sm text-muted-foreground">
            Permissions: {me.permissions.length ? me.permissions.join(', ') : 'none'}
          </p>
        </div>
      ) : null}
    </div>
  )
}

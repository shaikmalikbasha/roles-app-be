import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_app/users')({
  component: Users,
})

function Users() {
  return (
    <div className="px-6 py-8">
      <h2 className="mb-4 text-xl font-semibold">Users</h2>
      <p className="text-muted-foreground">Coming soon</p>
    </div>
  )
}

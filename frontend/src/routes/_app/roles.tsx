import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_app/roles')({
  component: Roles,
})

function Roles() {
  return (
    <div className="px-6 py-8">
      <h2 className="mb-4 text-xl font-semibold">Roles</h2>
      <p className="text-muted-foreground">Coming soon</p>
    </div>
  )
}

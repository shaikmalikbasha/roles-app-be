import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_app/permissions')({
  component: Permissions,
})

function Permissions() {
  return (
    <div className="px-6 py-8">
      <h2 className="mb-4 text-xl font-semibold">Permissions</h2>
      <p className="text-muted-foreground">Coming soon</p>
    </div>
  )
}

import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/')({
  component: Home,
})

function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <h1 className="text-2xl font-semibold text-foreground">Roles App</h1>
    </div>
  )
}

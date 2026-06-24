# Frontend — CLAUDE.md

React 19 + Vite + TypeScript SPA admin UI. Package manager: **Bun**.

## Commands

```bash
cd frontend

bun run dev          # dev server
bun run build        # tsc + vite build (use this to validate before PR)
bun run preview      # preview production build
```

---

## Stack

| Tool | Purpose |
|------|---------|
| React 19 + Vite | UI + bundler |
| TanStack Router | File-based routing (`src/routes/`) |
| TanStack Query | Server state / data fetching |
| TanStack Table | Data tables (installed, use for DataTable component) |
| shadcn/ui + Tailwind CSS | Component library + styling |
| Lucide React | Icons |
| Bun | Runtime + package manager |

Install shadcn components: `bunx shadcn add <component>`

---

## Structure

```
src/
  routes/
    __root.tsx          — root layout
    index.tsx           — redirects / → /dashboard or /login
    login.tsx           — /login (public)
    _app.tsx            — pathless layout: sidebar + auth guard
    _app/
      dashboard.tsx     — /dashboard
      users.tsx         — /users
      roles.tsx         — /roles
      permissions.tsx   — /permissions
  components/ui/        — shadcn components
  lib/
    api.ts              — ALL fetch calls go here, nowhere else
    auth.ts             — getToken / setToken / clearToken / isAuthenticated
    queryClient.ts      — React Query config
    utils.ts            — cn() helper
  main.tsx
```

---

## Standards

- All API calls go through `src/lib/api.ts` — never call `fetch` directly in components
- Use `useMutation` + `useQuery` from TanStack Query for all data operations
- Invalidate relevant query keys after every mutation so tables refresh automatically
- TanStack Router handles auth redirects via `beforeLoad` in `_app.tsx` — no ad-hoc `useEffect` guards
- Components are **named exports**, not default exports
- Use `cn()` from `lib/utils.ts` for conditional classNames

## Route Tree

TanStack Router auto-generates `src/routeTree.gen.ts` via the Vite plugin.  
If `bun run build` fails with unknown route keys, run `bun run vite build` first to regenerate it, then re-run `bun run build`.

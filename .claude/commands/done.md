# /done — Ship the current issue

Run this after finishing an issue. It handles the full PR workflow in order.

## Steps

1. **Lint + build** — stop if either fails and fix first
   - Backend: `cd backend && ruff check . && ruff format .`
   - Frontend: `cd frontend && bun run build`
   - Run only the half that was changed

2. **Commit** — stage relevant files, write a message referencing the issue: `feat: ... Closes #N`

3. **Push** — `git push -u origin <branch>`

4. **Open PR** — `gh pr create` with summary + test plan

5. **Close issue** — comment what was done, then `gh issue close N`

6. **Update CLAUDE.md** — mark the issue ✅ Done, set the next one ⬜ Next, commit directly to the branch

## Notes
- Do not skip the lint/build step
- Do not amend existing commits — create a new one for the CLAUDE.md update
- The CLAUDE.md issue table is the only thing to update; do not change architecture docs

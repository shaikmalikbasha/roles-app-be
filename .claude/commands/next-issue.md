# /next-issue — Show the next issue to work on

Fetch and display the next issue marked ⬜ Next in CLAUDE.md, then prepare to implement it.

## Steps

1. Run `gh issue list --repo shaikmalikbasha/roles-app-be --state open` to get current open issues
2. Cross-reference with the CLAUDE.md issue table to find what is marked ⬜ Next
3. Run `gh issue view <N> --repo shaikmalikbasha/roles-app-be` to fetch the full issue body
4. Display: issue number, title, full description
5. Suggest the branch name following the project convention
6. Ask the user if they want to start implementing it

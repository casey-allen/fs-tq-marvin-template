---
description: Commit and push your Obsidian vault to git
---

# /notes - Sync Your Obsidian Vault

Stage, commit, and push your Obsidian notes so they're backed up and synced.

## Instructions

### 1. Get Vault Path

Read `config.yaml` for the `obsidian_vault` path.

If `obsidian_vault` is empty or missing:
> "I don't know where your Obsidian vault is. Set it up with `/guide obsidian`, or tell me the path and I'll update your config."

### 2. Verify It's a Git Repo

```bash
cd {obsidian_vault} && git rev-parse --is-inside-work-tree
```

If not a git repo:
> "Your Obsidian vault at `{path}` isn't a git repository. Want me to initialize one? I can also help you connect it to a GitHub repo for backup."

If yes, offer to run `git init`, then ask if they want to add a remote.

### 3. Check for Changes

```bash
cd {obsidian_vault} && git status --short
```

If no changes:
> "Your notes are already up to date — nothing to commit."

Stop here.

### 4. Show What Changed

Display a brief summary:
```bash
cd {obsidian_vault} && git diff --stat
```

Show something like:
> **Notes updated:**
> - 3 files changed (Daily/2026-03-28.md, Permanent/priorities.md, Fleeting/quick-note.md)
> - 1 new file (Meetings/standup-2026-03-28.md)

### 5. Stage and Commit

```bash
cd {obsidian_vault} && git add -A && git commit -m "Update notes — {date}"
```

Use today's date in the commit message (e.g., "Update notes — 2026-03-28").

### 6. Push

Check if a remote exists:
```bash
cd {obsidian_vault} && git remote get-url origin
```

If a remote exists, push:
```bash
cd {obsidian_vault} && git push
```

If no remote:
> "Committed locally. Your vault doesn't have a remote set up, so I can't push. Want me to help you connect it to GitHub for backup?"

### 7. Confirm

> "Notes synced! {N} files committed and pushed."

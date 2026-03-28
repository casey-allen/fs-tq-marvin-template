---
description: Sync updates from the MARVIN template
---

# /sync - Get Updates

Pull new features and commands from the upstream MARVIN template into your workspace.

## Instructions

### 1. Check Upstream Remote

Verify the `upstream` remote exists:
```bash
git remote get-url upstream
```

If this fails, add it:
```bash
git remote add upstream git@github.com:fluidstackio/fs-tq-marvin-template.git
```

### 2. Fetch Updates

```bash
git fetch upstream
```

### 3. Show What's Changed

Compare the current branch with upstream:
```bash
git log HEAD..upstream/main --oneline
```

If there are no new commits, tell the user:
> "You're already up to date! No new changes in the template."

If there are new commits, show a summary:
```bash
git diff --stat HEAD..upstream/main
```

Display something like:

```
## Updates Available

**New/changed files:**
- .claude/commands/newcommand.md (new)
- .claude/skills/existing-skill.md (updated)
- skill-blueprints/team-digest/SKILL.md (updated)

Your personal files (config.yaml, CLAUDE.md, sessions/, etc.) won't be overwritten
unless there's a merge conflict — and you always get to resolve those.
```

### 4. Merge Updates

Ask: "Would you like me to pull these updates in?"

If yes:
```bash
git merge upstream/main
```

### 5. Handle Merge Conflicts

If there are merge conflicts:

**For personal files** (`config.yaml`, `CLAUDE.md`):
> "There's a conflict in {file}. Since this is your personal file, I'll keep your version."

Resolve by keeping the user's version:
```bash
git checkout --ours {file}
git add {file}
```

**For template files** (`.claude/commands/`, `.claude/skills/`, etc.):
> "There's a conflict in {file}. The template has updates, but you've also customized this file. Want to keep yours, take the template version, or let me show you both so you can decide?"

Resolve based on user's choice.

After resolving all conflicts:
```bash
git commit -m "Merge upstream template updates"
```

### 6. Check Blueprint Updates

After merging, check if any skill blueprints changed:
```bash
git diff HEAD~1..HEAD --name-only -- skill-blueprints/
```

For each changed blueprint directory (e.g., `skill-blueprints/team-digest/`):
- Check if the user has a corresponding generated skill (e.g., `skills/team-digest/`)
- If they do:
  - Show what changed (brief summary)
  - Offer to regenerate: "The team-digest blueprint has been updated. Want me to regenerate your skill with the latest logic? Your config.yaml settings will be preserved."
  - If yes: Read `config.yaml`, regenerate the skill from the blueprint with config values substituted, show the diff, and write
  - If no: Note that their version is now custom

### 7. Check for New Guides

Read `config.yaml` for `guides_completed` list. Check `guides/` for guide files.

If there are guides not in `guides_completed`:
> "New guides available:
> - {guide name} — {description}
>
> Run `/guide {slug}` to walk through any of them."

### 8. Finish

After syncing:
> "All done! You now have the latest MARVIN features. Type `/help` to see what's available."

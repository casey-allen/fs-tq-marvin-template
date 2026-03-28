---
description: Quick checkpoint - save progress to Obsidian and session log
---

# /update - Quick Context Checkpoint

Lightweight save without ending the session. Use frequently to preserve context.

## Instructions

### 1. Load Configuration
Read `config.yaml` to get Obsidian vault path and directory settings.

### 2. Identify What Changed
Quickly scan the recent conversation (since last checkpoint or session start) for:
- Topics worked on
- Decisions made
- Files created or modified
- New tasks or completed items

Keep it brief. No full summary needed.

### 3. Append to Session Log
Get today's date: `date +%Y-%m-%d`

Append to `sessions/{TODAY}.md`:
```markdown
## Update: {TIME}
- {what was worked on, 1-3 bullets}
```

If file doesn't exist, create with header: `# Session Log: {TODAY}`

### 4. Sync to Obsidian Daily Note
Append to `{obsidian_vault}/{daily_notes_dir}/{TODAY}.md` under "Today's Focus":

- Tag completed items: `DONE: [MARVIN] {description}`
- Tag new actions: `ACTION: {description}`
- Tag new blockers: `BLOCKED: {description}`
- Tag decisions: add to a `## Decisions` section

If today's daily note doesn't exist, create it from `{obsidian_vault}/{templates_dir}/Daily Template.md`.

### 5. Update Priorities (if needed)
Only update `{obsidian_vault}/Permanent/priorities.md` if something material changed:
- New open thread
- Completed item
- Changed priority
- New task discovered

Skip if nothing material changed.

### 6. Staleness Check
Check the "Last updated" date in `{obsidian_vault}/Permanent/priorities.md`:
- If **3+ days old**: flag it and ask: "Priorities are {N} days stale. Want me to do a full refresh now or at /end?"
- If recent: proceed without comment

### 7. Confirm (minimal)
One line: **"Checkpointed: {brief description}"**

No summary. No "next actions" list. Just confirm the save.

---
description: End MARVIN session - save context to Obsidian and session log
---

# /end - End MARVIN Session

Wrap up the current session and save all context for continuity.

**The goal:** A fresh session tomorrow should read `{obsidian_vault}/Permanent/priorities.md` and today's daily note and know exactly where things stand.

## Instructions

### 1. Load Configuration
Read `config.yaml` to get Obsidian vault path and directory settings.

### 2. Summarize This Session
Review the conversation and extract:
- **Topics discussed** - What did we work on?
- **Decisions made** - What was decided and why?
- **Open threads** - What's unfinished or needs follow-up?
- **Action items** - What needs to happen next?

### 3. Update Session Log
Get today's date with `date +%Y-%m-%d`.

Append to `sessions/{TODAY}.md` (create if it doesn't exist):
```markdown
## Session End: {TIME}

### Topics
- {topic 1}
- {topic 2}

### Decisions
- {decision and reasoning}

### Open Threads
- {thread 1}

### Next Actions
- {action 1}
```

If creating a new file, add header: `# Session Log: {TODAY}`

### 4. Update Obsidian Daily Note
Append to `{obsidian_vault}/{daily_notes_dir}/{TODAY}.md` under "Today's Focus":

- Tag completed items: `DONE: [MARVIN] {description}`
- Tag new actions: `ACTION: {description}`
- Tag new blockers: `BLOCKED: {description}`
- Tag new delegations: `DELEGATE: @{person} {description}`

If today's daily note doesn't exist, create it from `{obsidian_vault}/{templates_dir}/Daily Template.md`.

### 5. Log Decisions in Daily Note
If decisions were made, append to today's daily note:
```markdown
## Decisions
- **{Topic}**: {What was decided} — {Why}
```

### 6. Update Priorities (MANDATORY)
This is the most important step. Read `{obsidian_vault}/Permanent/priorities.md`:

**If 3+ days stale (or no timestamp):** Do a full rewrite.
- Re-read the last 3 days of session logs and daily notes
- Rebuild priorities, open threads, and project statuses from scratch
- Ensure nothing is carried forward that's already resolved

**If recent (updated within 3 days):** Do an incremental update.
- Mark completed items as done or remove them
- Add new priorities and open threads
- Update the "Recent Context" section with the last 5 session entries
- Shift priorities based on what emerged this session

**Always:**
- Update the "Last updated: {TODAY}" line
- Ensure open threads reflect reality (remove resolved, add new)
- Ensure priorities are ordered by actual urgency

### 7. Confirm
Show a brief summary:
- What was logged to session log and daily note
- Key items for next session
- Priorities update confirmation (incremental or full refresh)

Keep it concise.

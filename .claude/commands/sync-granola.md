---
description: Pull Granola meeting notes into Obsidian (Meetings/ + tagged action items in daily note)
---

# /sync-granola - Sync Granola meetings into Obsidian

Pull recent Granola meeting notes into the Obsidian vault. One-way: Granola → Obsidian.

## Instructions

### 1. Setup
- Read `config.yaml` for `obsidian_vault` (vault path).
- Run `date +%Y-%m-%d` for TODAY.
- Default range: **today's meetings**. If the user specifies a range (e.g. "this week", "yesterday"), use that instead.

### 2. Pull meetings (Granola MCP)
- Use `list_meetings` (time_range matching the request; for "today" use a custom range of TODAY) to get the meeting list.
- For each meeting, use `get_meetings` / `get_meeting_transcript` to fetch the notes, summary, attendees, and any action items.

### 3. Write one note per meeting
For each meeting, create/update `{obsidian_vault}/Meetings/{YYYY-MM-DD}-{slug}.md` (slug = kebab-cased title):

```markdown
# {Meeting Title}

- **Date:** {YYYY-MM-DD HH:MM}
- **Attendees:** {names}
- **Deal/Project:** {link to relevant deal/site if identifiable}

## Summary
{Granola summary}

## Notes
{Granola notes / cleaned transcript highlights}

## Action Items
- ACTION: ...
- DELEGATE: @name ...
```

**Idempotent:** if the meeting note already exists, update it rather than duplicating. Skip meetings with no notes/transcript yet.

### 4. Surface action items into the daily note
- Append the meeting's action items as tagged lines (`ACTION:` / `DELEGATE:`) to `{obsidian_vault}/Daily/{TODAY}.md` under `## Notes`, each prefixed with the meeting name for context (e.g. `- ACTION: [Beacon Weekly] send revised model to Dermot`).
- Create today's daily note from the template if it doesn't exist.
- Do not duplicate action items already present in the daily note.

### 5. Link people
- If an attendee already has a `{obsidian_vault}/People/{name}.md` note, add a dated line referencing the meeting. Don't create new People notes unless asked.

### 6. Commit & push
```bash
cd {obsidian_vault} && git add -A && git commit -m "Granola sync {TODAY}" && git push
```

### 7. Report
Summarize what was synced: N meetings filed, M action items captured. List the meeting titles.

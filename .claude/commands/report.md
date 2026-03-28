---
description: Generate a weekly report from Obsidian notes and Jira
---

# /report - Weekly Report

Generate a summary of what you accomplished this week.

## Instructions

### 1. Load Configuration
Read `config.yaml` to get Obsidian vault path, Jira projects, and other settings.

### 2. Gather the Data

Run `date +%Y-%m-%d` to get today's date. Determine the date range (most recent Monday through today).

Read these sources:
- **Obsidian daily notes**: Read all files in `{obsidian_vault}/{daily_notes_dir}/` from the past 7 days
- **Session logs**: Read all files in `sessions/` from the past 7 days
- **Priorities**: Read `{obsidian_vault}/Permanent/priorities.md` for current priorities
- **Goals**: Read `{obsidian_vault}/Permanent/goals.md` to connect work to goals

Extract tagged items from daily notes:
- `DONE:` items → Accomplishments
- `BLOCKED:` items → Blockers
- `WAITING:` items → Vendor/procurement status
- `DELEGATE:` items → Delegation status
- `ACTION:` items still unchecked → Carry-forward

### 3. Pull Jira Status (if configured)

If `jira_projects` is set in config.yaml, query each project:
- Issues updated this week
- Issues completed this week
- Current blockers

### 4. Compile the Report

Create a report with these sections:

```markdown
# Weekly Report: Week of {DATE RANGE}

## Summary
- Top 3-5 accomplishments this week
- Focus on outcomes, not activities

## Shipped
- Specific deliverables completed (from DONE tags and Jira)
- If nothing shipped, omit this section

## Key Activities
- Organized by project or workstream
- Include problems solved, progress made, work in flight

## Decisions Made
- Key decisions from daily notes this week
- Include the context/reasoning for each

## Progress on Goals

| Goal | Status | This Week |
|------|--------|-----------|
| {Goal from goals.md} | {On track / Behind / Ahead} | {What happened toward this goal} |

## Blocked / Waiting

| Item | Blocker | Since | Jira |
|------|---------|-------|------|
| {from BLOCKED/WAITING tags} | {who/what} | {date} | {link if exists} |

## Open Threads
- Anything unfinished or waiting on others
- Decisions still needed
- Carry-forward ACTION items

## Looking Ahead
- Top priorities for the coming week
- Carries forward from open threads
- Any upcoming deadlines or events
```

### 5. Save the Report

Save to `reports/{TODAY}.md` using today's date.

Create the `reports/` directory if it doesn't exist.

### 6. Offer Next Steps

Ask: "Want me to copy this somewhere, adjust the tone, or focus on specific areas?"

Common follow-ups:
- Copy to clipboard for pasting into Slack or email
- Adjust tone (more formal for managers, casual for team)
- Save to Obsidian Weekly/ folder
- Focus on specific projects or goals

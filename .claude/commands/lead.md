---
description: Capture, update, or re-score a BD lead in the shared Master Lead Tracker — plain-English, pulls its own context (Granola/email/Drive). Follows John's tracker playbook.
---

# /lead — BD Lead Intake & Living Updates

Front of the funnel for the **shared Master Lead Tracker** (a team system owned by john@fluidstack.io). The sheet is the home — no Obsidian lead notes. **You never have to paste context**: tell `/lead` in plain English and it fetches the source itself (Granola transcript, email thread, Drive doc).

**Usage:**
- `/lead <pasted text / Drive link / PDF>` — log a new lead
- `/lead sweep` — run intake + update sweep now (same as scheduled `bd-lead-sweep`)
- `/lead update <who>` — e.g. `update Frontera from my call` → find the lead, pull the Granola/email context, apply changes
- `/lead <plain-English change>` — `"Frontera is 300MW online 2027"`, `"move Pen Holdings to Qualified"`, `"set L-009 land score to 5"`
- `/lead` alone — ask what/where

## ⚠️ Shared system — follow John's playbook
Read John's **"Master Tracker Claude Context Pack"** (`Business Development / Project Leads / Instructions/`, Drive id `1ZULUPhgHbvfyBSc-ZtfiDCCd1hdPbm-6`) — it's canonical. The full column map, scoring rules, write mechanics, and **John's conventions** are also documented in the `bd-lead-sweep` skill (`~/.claude/scheduled-tasks/bd-lead-sweep/SKILL.md`) — follow those exactly. Non-negotiables:
- **Stage dropdown:** `Lead → Discovery → VDR/RFI Review → Qualified → Progressed → Killed` (nothing else).
- **DRI:** exactly `John` or `Casey`.
- **Missing text/date/number → `N/A`** (never blank/guessed). **Score cell with nothing to go on → leave blank** (not N/A) and say why in Notes; otherwise always score with a one-line rationale.
- **Discovery Score = John's weighted SUM formula** (do NOT substitute a normalized one — that's a pending Casey↔John discussion).
- **Never overwrite the formula columns** H/I/J/AK/AW/AX/AY; write Date Added (C) + Last Updated (U) explicitly (onEdit doesn't fire on API writes). Never write `""` into a score cell (breaks the weighted-sum formula) — write only populated score cells.
- **`Status` (col B)** = `Pursuing`/`Passed`/`On Hold` (dropdown, colour-coded) — set it on every new lead and keep it in sync with Stage (`Killed` ⇒ `Passed`).
- **Power Timeline milestones:** `First Power / Ramp 2 / Ramp 3 / Ramp 4 / Full Build`; Grid/BTM tracked separately; a `Full Build` row per source drives the MW pull (H/I/J).
- **Contact = the one current point of contact**, not every attendee.
- Don't add columns or change John's schema/dropdowns without Casey/John sign-off. (Casey added `Status` at B on 2026-07-20 — schema is now A–AZ, 52 cols; John's Context Pack still shows the old A–AY.)

## Config (`config.yaml`)
`leads_tracker_sheet_id` = `1mSDdIeERKPoBeaOa_T7lHi5MA4aSOyndz7-Bfd_VfZg`; tabs `Lead Tracker` / `Power Timeline`. Per-lead Drive folders live in `Business Development / Leads/` (id `1NgvXUEbd3AwFGIuvHn_YfFy-HM39DVdn`). `lead_outreach` = RFI/NDA draft settings.

## Mode A — NEW lead
1. **Resolve the source** (paste / Drive doc / or go pull the named email/call yourself).
2. **Extract + score** per John's rules above. Assign next `L-NNN`.
3. **Show the card and CONFIRM** before writing (interactive). Let the user correct inline.
4. **Write** on approval: Power Timeline rows, then the Lead Tracker row (data + copy formulas from an existing row). Create the Drive folder (`<Lead ID> <Project> (<place>)/` + `Seller Docs/`, copy master RFI) and put the folder URL in Notes.
5. **RFI/NDA draft reply** if `lead_outreach.enabled` + identifiable sender (standalone Gmail DRAFT, never sent; skip if Casey already replied in-thread).

## Mode B — UPDATE an existing lead
Identify the lead → **pull the Granola/email context yourself** → apply changes → **log in Notes** (`YYYY-MM-DD: <change> per <source>`) → set Last Updated. Briefly confirm interactively; report the new Discovery/Rank if it moved.

## Mode C — Score override
Score cells (AC–AJ Discovery, AM–AV RFI) are manual — the user can overwrite any. On `"set <lead> <category> score to N"`, write that cell (weighted SUM recomputes) and log it in Notes. Never revert a manual score on a sweep. To mark RFI-reviewed: set `RFI Reviewed? = Yes` and fill the 10 RFI scores (propose from the RFI/data room; user confirms).

## Mode D — sweep
Run the `bd-lead-sweep` logic now (intake + update).

## Notes
- Front-of-funnel only; graduates via `/vdr` → Kaiser (Stage `Qualified`/`Progressed`). Confirm before writing interactively; the scheduled sweep writes directly. **No outbound messages are ever sent** — replies are drafts.
- Keep every lead; Stage `Killed` rather than delete.

---
description: Run the full inbound-deal diligence stack (VDR review + gap analysis + power evaluation) on a data room
---

# /vdr - Full VDR Diligence Stack

Run Fluidstack's complete inbound-deal diligence workup on a data room, in one pass. This orchestrates **three skills in sequence**, lands the deep outputs in the Obsidian vault, and publishes a **team-shareable deal-summary Artifact**.

**Output philosophy (revised 2026-07-21):** analysis is written once to `deal_data.json`; every deliverable is a *render* of that file. Per run, produce exactly: **1 Artifact + 1 Excel workbook + deal_data.json/summary.json**. The Word Executive Summary and standalone power-evaluation markdown are **on-demand only** — generate them when Casey asks or when something formal needs to be sent externally.

**Usage:** `/vdr <path-or-Drive-link>` — e.g. `/vdr ~/Downloads/Captus` or `/vdr https://drive.google.com/drive/folders/...`

If no path/link is given, ask the user for the data room location before proceeding.

## Instructions

### 1. Resolve the data room and project name
- Take the path or Drive link from the argument. Confirm it's readable (`ls -R <path>` for a local folder, or Google Drive search for a link).
- Derive a short **project codename** from the CIM/folder (e.g. "Captus / Project Switchyard" → `Captus-Switchyard`). Use it for the output folder and filenames.
- Set the output folder to the Obsidian vault `Projects/` directory (read `obsidian_vault` from `config.yaml`): `<vault>/Projects/<Codename>-VDR/`. Create it if absent.

### 2. Read the data room ONCE, then reuse
- Inventory every file; read the CIM/teaser first to anchor the deal, then read the rest. For large rooms (50+ files), fan out parallel subagents by document category (Power, Land/Title, Permitting/Zoning, Environmental/Geotech, Water, Gas, Fiber, Commercial) — each returns findings mapped to RFI/risk fields with citations.
- **Read this once.** All three skills below consume the same read — do not re-ingest per skill.

### 3. Run the analysis (all three skills), write deal_data.json first
Run the three skills' *analysis* against the single data-room read — **`vdr-review`** (RFI, 82-item risk matrix, Q&A log, deal record, scoring matrix, recommendation), **`gap-analysis`** (every diligence requirement marked Confirmed / Partial / Missing / N/A / Stale, with priority), and **`power-market-evaluator`** (extraction checklist, process position, firm-gate verdict, what-to-get-next, confidence labels).
- Write ALL findings to a canonical **`deal_data.json`** in the project folder before rendering anything. Deliverables below are renders of this file — never re-read the data room to build a deliverable.
- power-market-evaluator: if the ISO/market isn't in the skill database (e.g. **AESO/Alberta**), run "utility-not-in-database" mode, label outputs accordingly, and flag that a market record should be built.
- gap-analysis: if the bundled checklist/SOW aren't installed, reconstruct from skill methodology + the data-room read, and say so on the workbook's Cover sheet.

### 4. Render deliverable 1 — the Excel workbook
One workbook, `<Codename>-VDR-Tables.xlsx`, containing the vdr-review sheets (Inventory, RFI, Risk Matrix, Q&A Log, Deal Record, Scoring Matrix) **plus the gap matrix as an additional sheet** (no separate gap-analysis file). Keep the workbook's existing black-and-white formal formatting — it's the deep-dive reference.

**Style rules (Casey, 2026-07-22): concise and human, every sheet.**
- **Q&A Log:** each question is ONE clarified sentence a busy reader can act on — no paragraphs, no preamble, no over-explanation. Answers/status likewise one line. Background reasoning lives in `deal_data.json`, not the sheet.
- **Risk Matrix / Gap Matrix:** descriptions ≤ ~15 words; put the "so what" in the rating/priority columns, not prose.
- Cell text is scannable: no nested clauses, no citations mid-sentence (use a reference column), no ALL-CAPS emphasis walls.
- If a row needs a paragraph to be understood, the row is wrong — split it or push detail to deal_data.json.

**Distribution:** after rendering, upload a copy of the workbook to the deal's Google Drive folder (the FS-controlled deal directory — NEVER a folder shared with the counterparty; check sharing before upload). Record the Drive link in `summary.json` (`workbook_drive_url`) and link it from the artifact footer ("Deep dive: full workbook →"). The artifact is the front door; the workbook is the deep layer behind it.

### 5. Render deliverable 2 — the deal-summary Artifact (team-shareable)
Publish a **private Claude Artifact**. **Audience (per Casey, 2026-07-22): someone who has never heard of the project.** It is a two-minute orientation, NOT an analyst dashboard — the workbook carries the analytical depth. Template: the Pyote page (`https://claude.ai/code/artifact/1193d95f-fbaf-4996-9ae8-a358e6bcc070`, source in the project folder's `*-Summary.html`). Structure:
1. **Header** — project name, one plain-language subtitle (what/where/size), 2-3 status pills (deal stage, target first power).
2. **"What this is"** — two short paragraphs: the site, the parties, the deal shape, why it's interesting, what the work is proving. No acronyms without translation.
3. **Power section** (power is always shown; per Casey 2026-07-22): plain-language verdict chip + **process-position tracker** (5 stages, plainly named, status-marked) + **MW ladder** (marketed → demonstrated → contracted; ~3 rungs — make the marketing-vs-reality gap visible without jargon).
4. **Two-up: "Why we're pursuing it" / "What has to get solved"** — 4-6 plain-English bullets each. This replaces risk tables, scores, and conditions on the page.
5. **Key facts grid** (~9 rows) + **Update log** (dated one-liners, newest first — living page, same URL) + footer pointing the deal team to the workbook/_findings/deal_data.json.
- **Do NOT put on the page:** the numeric score, conditions-for-advance, gap-matrix tables, the 82-item risk framework, or acronym-dense findings. All of that lives in the workbook and `summary.json` for the deal team.
- The power firm-gate verdict lives in the Power section, translated to plain language — no standalone power markdown by default.
- Build with the `artifact-design` + `dataviz` skills' guidance (theme tokens for light/dark, status colors reserved for state, tabular-nums). Save the HTML into the project folder too (`<Codename>-Summary.html`) so the source is versioned with the deal.
- **First run of a deal mints the URL; every later update MUST redeploy to the same URL** (pass `url` to the Artifact tool from other conversations). Record the URL in `summary.json` and the project note. The artifact stays private — Casey shares it from the page's share menu.

### 6. Write summary.json
Drop a small **`summary.json`** next to deal_data.json (schema template: `Projects/GDA - Pyote TX/summary.json`, `schema_version: 1`): codename, seller, market/ISO, MW, stage, score, recommendation, top risk, gap counts, review date, artifact URL, slack channel, kaiser site id, and `status: "active"`. This registers the deal for **`/deal` refreshes and the weekly sweep**, and is the feedstock for the future portfolio roll-up — keep the schema stable.

### 7. Closeout
- Confirm the project folder holds: `deal_data.json`, `summary.json`, the workbook, and `<Codename>-Summary.html`; confirm the Artifact published.
- Give the user: the recommendation + score, gap counts (Confirmed/Partial/Missing), the power firm-gate verdict, the top 3–5 things to chase, and the artifact URL.
- Flag any skill that ran degraded (missing bundled files, missing market profile) so coverage gaps are visible.
- Offer (don't auto-generate): formal Word Executive Summary or standalone power-evaluation markdown, if something needs to go external.

## Notes
- **Confirm before any outbound action.** This command only reads and writes local/vault files — it does not send the RFI to the broker or post anywhere. Offer that as a follow-up.
- Be conservative throughout: "Not in VDR" is a flag, never neutral. Treat seller timelines as optimistic until third-party confirmed.
- All three skills share the single data-room read from step 2.

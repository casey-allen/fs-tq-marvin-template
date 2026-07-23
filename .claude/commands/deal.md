---
description: "Refresh a deal's summary artifact from live context (Slack/Granola/Gmail/Kaiser), or sweep all active deals"
---

# /deal - Keep deal-summary Artifacts current

The deal-summary Artifacts are the team's **source of truth** per project. They only stay true if they're refreshed as context changes. This command is the refresh engine — it does NOT re-read the data room (that's `/vdr`); it ingests what's changed *around* the deal and redeploys the page.

**Usage:**
- `/deal refresh <codename>` — refresh one deal (e.g. `/deal refresh pyote`)
- `/deal sweep` — refresh every active deal (this is what the weekly scheduled task runs)

## How deals are registered

There is no separate registry. A deal is "registered" by having a **`summary.json`** in its project folder: `<vault>/Projects/*/summary.json` (read `obsidian_vault` from `config.yaml`; vault is `/Users/casey/git/obsidian`). `status: "active"` makes it sweep-eligible; set `status: "dormant"` or `"dead"` to stop sweeping without deleting anything. `/vdr` creates this file for new deals; backfilled deals get one by hand.

## Instructions — `refresh <codename>`

### 1. Locate and load
- Glob `<vault>/Projects/*/summary.json`, match `codename` case-insensitively (substring OK). If ambiguous or not found, list candidates and stop.
- Read `summary.json`, `deal_data.json` (may be absent on backfilled deals — then the project's same-named `.md` note is the data source), and the archived `*-Summary.html`.

### 2. Gather deltas since `last_updated`
Query each source **best-effort, in parallel** — a failed source is reported, never fatal:
- **Slack:** read the deal channel (`slack_channel_id`) since `last_updated`; capture decisions, document arrivals, date changes, counterparty behavior.
- **Granola:** meetings since `last_updated` mentioning the codename/counterparty; pull action items and stated status changes.
- **Gmail:** threads with the counterparty contacts / advisor since `last_updated`.
- **Kaiser:** the site record (`kaiser_site_id`) — stage, milestones, risks, diligence summary changes.

### 3. Apply
- **No material changes** → do NOT republish. Update `last_updated` in `summary.json` and report "checked, no change."
- **Changes found** → update `deal_data.json` (or the `.md` note) with the new facts; update the HTML render: affected sections, the **as-of banner**, and **prepend an Update log entry** (date + 1-line what-changed, newest first, keep ~8 rows). Facts change freely; if a delta warrants moving a **verdict, gate, or risk ranking**, apply it but flag it prominently in the digest (step 5) — those are the judgment calls Casey audits.
- Keep the layout contract of the archived HTML (verdict banner → Power tracker + MW ladder → KPI cards → risks → diligence scorecard → chase list → update log → deal facts). Never restructure during a refresh.

### 4. Redeploy — same URL, always
- Publish via the Artifact tool passing `url: <summary.json artifact_url>`. **Never mint a new URL for an existing deal.** Label the version `refresh-YYYY-MM-DD`.
- Save the updated HTML back to the project folder (`summary_html`), update `summary.json` (`last_updated`, `data_as_of`, any changed rollup fields).

### 5. Report
DM Casey (Slack) a short digest: deal, what changed, what was flagged, artifact link. **Auto-publish is pre-approved for this flow (Casey, 2026-07-22)** — publish first, digest after. Exception: anything that would go to a channel or an external party still requires explicit confirmation; this flow only ever DMs Casey.

## Instructions — `sweep`

1. Glob all `summary.json` with `status: "active"`. Order by oldest `last_updated` first. **Cap at 6 deals per run** (same wall-clock lesson as lead-inbox); note any skipped deals in the digest.
2. Run the `refresh` procedure for each.
3. Send ONE combined DM digest: per deal — changed / no change / source errors, with flags called out on top. If a deal's refresh dies, continue with the rest.
4. If the vault has uncommitted changes from the sweep, leave them uncommitted — Casey commits via `/notes`.

## Notes
- The artifact is a **render**; `deal_data.json` (or the note) is canonical on disk. Never edit the page without writing the underlying fact back to the data file.
- **Pairing with the workbook:** the artifact and `<Codename>-VDR-Tables.xlsx` render from the same `deal_data.json` — page always current, workbook current-as-of-last-render. A refresh updates the JSON but does not rebuild the xlsx; if a refresh changes diligence-relevant fields (Q&A answers, gap statuses, risk ratings), say so in the digest so Casey can trigger a workbook re-render. If the workbook has a Drive copy (`workbook_drive_url`), a re-render must update that copy too.
- Staleness must be visible: the as-of banner and update log are load-bearing, not decoration. A refresh that finds nothing still proves the page was checked — that's why `last_updated` moves.
- Conservative bias carries over from `/vdr`: seller claims stay labeled as claims until third-party confirmed.

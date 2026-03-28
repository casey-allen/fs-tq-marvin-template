---
name: guide-keeping-updated
description: >
  Guide to keeping MARVIN skills, Codex plugins, and the template itself
  up to date. Triggers on: "/guide keeping-updated", "how do I update MARVIN",
  "how do I update skills", "walk me through updates".
---

# Keeping MARVIN Updated

> **Reading this on GitHub?** Follow the steps below at your own pace.
> **Inside MARVIN?** Say `/guide keeping-updated` and I'll walk you through it.

## Prerequisites

- MARVIN set up and running (complete [Guide 01](01-getting-started.md) first)

## What You'll Learn

How to keep three things up to date:
1. **MARVIN template** — new commands, skills, and guides
2. **Codex plugins** — company-wide skills like NRFC writer
3. **Your personal skills** — team digest, weekly review, etc.

## 1. MARVIN Template Updates (`/sync`)

The MARVIN template (`fs-tq-marvin-template`) gets updated with new features, commands, and guides. To pull updates into your fork:

Inside MARVIN:
```
/sync
```

**What `/sync` does:**
- Fetches the latest from the upstream template repo (`git fetch upstream`)
- Merges new commits into your local branch (`git merge upstream/main`)
- Shows you what changed
- **Your personal files are safe** — `config.yaml`, `CLAUDE.md`, `sessions/`, etc. won't be overwritten unless there's a merge conflict, and you always get to resolve those

**You can also do it manually:**
```bash
git pull upstream main
```

**How often:** Weekly, or when you hear about new features. MARVIN will mention available updates when it detects them.

## 2. Codex Plugin Updates

Codex skills (NRFC writer, RFC crafter, etc.) are managed separately through the Claude Code plugin system.

**Check for updates:**
```bash
claude plugin marketplace update
```

**Update a specific plugin:**
```bash
claude plugin update codex-document-skills
```

**How often:** Monthly, or when you notice a skill behaving differently than expected.

## 3. Skill Blueprint Updates

When the template gets updated skill blueprints (improved team digest logic, better weekly review format, etc.), `/sync` will detect this and offer to regenerate your personal skills:

> "The team-digest blueprint has been updated. Would you like me to regenerate your skill with the latest logic? Your configuration (Jira projects, Slack channels, etc.) will be preserved."

If you accept:
- MARVIN reads your `config.yaml` for your personal settings
- Regenerates the skill from the updated blueprint
- Shows you a diff of what changed
- Writes the updated skill files

If you decline:
- Your current skill stays as-is
- MARVIN notes that your version is now custom

## 4. Manual Skill Editing

You can always edit your skills directly:

- `skills/team-digest/SKILL.md` — Change the process, add steps
- `skills/team-digest/prompts/system_prompt.md` — Tune the analysis methodology
- `skills/team-digest/prompts/agent_instructions.md` — Adjust the output format
- `skills/weekly-review/SKILL.md` — Customize the review process

**Important:** If you manually edit a skill, blueprint updates won't overwrite your changes unless you explicitly ask MARVIN to regenerate.

## 5. Adding New Skills

Want a new capability? You have several options:

- **Use the skill creator:** Tell MARVIN "I want a skill that does X" and it'll help you build one
- **Copy a blueprint:** Look at `skill-blueprints/` in the template for examples
- **Install from Codex:** Check if someone has already built what you need — `claude plugin list` shows available skills

## Quick Reference

| What | How | How Often |
|------|-----|-----------|
| Template updates | `/sync` (or `git pull upstream main`) | Weekly |
| Codex plugins | `claude plugin marketplace update` | Monthly |
| Blueprint regeneration | MARVIN offers during `/sync` | When blueprints change |
| Manual skill edits | Edit files in `skills/` | Anytime |

## Troubleshooting

**"/sync says no upstream remote"** — Add the upstream remote: `git remote add upstream git@github.com:fluidstackio/fs-tq-marvin-template.git`

**Merge conflicts during /sync** — MARVIN will help you resolve these. Your personal files (`config.yaml`, `CLAUDE.md`) always take priority. For template files, you choose which version to keep.

**"marketplace update" fails** — Run `claude plugin marketplace list` to check if the Codex marketplace is registered. If not, re-add it: `claude plugin marketplace add fluidstackio/codex`

**Skill regeneration lost my customizations** — If you manually edited a skill and then regenerated, the manual edits are gone. Check git history: `git log --oneline skills/` to find and restore previous versions.

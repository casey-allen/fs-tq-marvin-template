---
description: Manage skills — list installed, install from Codex marketplace, check for updates
---

# /skills - Skill Management

Manage MARVIN skills and Codex marketplace plugins.

**Argument:** `$ARGUMENTS` (expects a sub-command: `list`, `install`, `update`, `search`)

## Sub-Commands

### No argument / help

Show available sub-commands:
```
/skills list              Show installed skills (workspace + Codex plugins)
/skills install <plugin>  Install a Codex plugin (e.g., codex-document-skills)
/skills update            Check for and apply skill updates
/skills search <query>    Search for skills in the Codex marketplace
```

### `list`

Show all installed skills from both sources:

**1. Workspace skills** — List files in `skills/` directory:
```bash
ls -d skills/*/SKILL.md 2>/dev/null
```

**2. Codex marketplace plugins** — List installed plugins:
```bash
claude plugin list
```

Present results grouped by source:

```
## Installed Skills

### Workspace Skills (personal)
- team-digest — Daily team engineering digest
- weekly-review — Weekly review and planning

### Codex Plugins (company-wide)
- codex-document-skills — NRFC writer, RFC crafter, PRD crafter, markdown formatter

No skills? Run /guide skills-and-mcp to get started.
```

### `install <plugin>`

Install a plugin from the Codex marketplace.

1. If the Codex marketplace isn't registered yet:
   ```bash
   claude plugin marketplace add fluidstackio/codex
   ```
2. Install the requested plugin:
   ```bash
   claude plugin install <plugin>
   ```
3. Confirm success: "Installed! Restart MARVIN for the new skills to appear."

**Available plugins:**
- `codex-document-skills` — NRFC writer, RFC crafter, PRD crafter, markdown formatter
- `codex-frontend-skills` — Frontend PR workflow

### `update`

Check for updates to both Codex plugins and workspace skill blueprints.

**1. Codex marketplace:**
```bash
claude plugin marketplace update
```

If updates are available, list them and ask: "Update all, or pick specific ones?"

**2. Workspace skill blueprints:**
Read `.marvin-source` to find the template directory. Compare `skill-blueprints/` in the template with `skills/` in the workspace.

If blueprint updates are available:
- Show what changed
- Offer to regenerate skills from updated blueprints + config.yaml
- Never overwrite without confirmation

### `search <query>`

Search the Codex marketplace for matching skills:

```bash
claude plugin marketplace list
```

Filter results by query and present matches. If no match, suggest checking the Codex repo directly.

## Notes

- Codex marketplace: `fluidstackio/codex` (private, requires GitHub access)
- Workspace skills live in `skills/` and are generated via `/guide`
- Codex plugins are managed by Claude Code's plugin system, separate from workspace skills
- Run `/guide skills-and-mcp` for a full walkthrough of the skills ecosystem

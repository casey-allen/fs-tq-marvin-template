# MARVIN - AI Chief of Staff for Infrastructure Engineers

**MARVIN** = Manages Appointments, Reads Various Important Notifications

An AI Chief of Staff built on Claude Code for the Fluidstack Infrastructure org. MARVIN integrates with Jira, Slack, Confluence, GitHub, Google Calendar, and Obsidian to give you a daily operating rhythm: morning briefings, task tracking, team digests, and weekly reviews.

No coding experience required — MARVIN walks you through setup interactively.

## Who is this for?

Anyone in the Infrastructure org:
- **Network Engineers** — track deployments, circuit turn-ups, operations, and automation work
- **Program Managers** — cross-team dependencies, delivery tracking, risk management
- **ICT Architects** — design reviews, standards compliance, technology evaluation

Setup includes role-based defaults that pre-configure your Jira projects, Slack channels, and workstreams.

## Quick Start

```bash
# Clone the template
git clone git@github.com:fluidstackio/fs-tq-marvin-template.git
cd fs-tq-marvin-template

# Run interactive setup
./.marvin/setup.sh
```

Setup takes about 5 minutes and creates a personal workspace with your profile, config, and shell aliases.

Then open a new terminal and type `marvin` to start. Inside MARVIN, type `/guide` to walk through additional setup.

## What You Get

### Daily Workflow

Start your day with `/start` for a briefing: priorities, Jira status, blockers, and carry-forward items from your Obsidian notes. Work naturally throughout the day — capture tasks, delegations, and notes. End with `/end` to save everything.

### Interactive Guides

MARVIN includes 6 setup guides that walk you through capabilities step by step:

| Guide | What It Covers |
|-------|---------------|
| [Getting Started](guides/01-getting-started.md) | Install Claude Code, clone template, run setup |
| [Skills & MCP](guides/02-skills-and-mcp.md) | Codex marketplace, company skills (NRFC writer, etc.) |
| [Obsidian Vault](guides/03-obsidian-vault.md) | Git-tracked second brain with daily notes and task tracking |
| [Team Digest](guides/04-team-digest.md) | Daily Jira/Slack/GitHub synthesis posted to your team's Slack |
| [Weekly Review](guides/05-weekly-review.md) | Weekly planning with Obsidian notes + Jira project pulse |
| [Keeping Updated](guides/06-keeping-updated.md) | /sync, marketplace updates, blueprint regeneration |

Run `/guide` inside MARVIN to start any guide interactively.

### Commands

| Command | What It Does |
|---------|--------------|
| `/start` | Start your day with a briefing |
| `/end` | End session and save everything |
| `/update` | Quick checkpoint (save progress) |
| `/guide` | Interactive setup walkthroughs |
| `/skills` | Manage Codex plugins and workspace skills |
| `/report` | Generate a weekly summary |
| `/commit` | Review and commit git changes |
| `/status` | Check integration and workspace health |
| `/sync` | Get updates from the template |
| `/help` | Show all commands and integrations |

### Integrations

| Integration | What It Provides |
|-------------|------------------|
| [Atlassian](.marvin/integrations/atlassian/) | Jira, Confluence |
| [Google Workspace](.marvin/integrations/google-workspace/) | Gmail, Calendar, Drive |
| [Microsoft 365](.marvin/integrations/ms365/) | Outlook, Calendar, OneDrive, Teams |
| [Slack](.marvin/integrations/slack/) | Channel monitoring, posting |
| [Parallel Search](.marvin/integrations/parallel-search/) | Web search |

Integrations are configured during onboarding. Type `/status` to check health.

## How It Works

Fork the template, personalize it, and work directly in your fork:

```
fs-tq-marvin-template/            Your fork (everything in one repo)
├── CLAUDE.md                     Your profile and preferences
├── config.yaml                   Jira projects, Slack channels, vault path
├── skills/                       Your personalized skills (team-digest, weekly-review)
├── sessions/                     Daily session logs
├── reports/                      Weekly reports
├── guides/                       Setup walkthroughs
├── skill-blueprints/             Skill templates with config placeholders
├── profiles/                     Role-based config presets
└── .marvin/                      Setup scripts and integrations

Obsidian vault (your second brain)
├── Daily/                        Daily notes with task tags
├── Weekly/                       Weekly review summaries
├── Permanent/                    Priorities and goals
└── People/                       Per-person tracking
```

State (priorities, goals, daily notes) lives in your Obsidian vault. Pull template updates via `/sync` (which merges from the upstream repo).

## Codex Skills

Company-wide skills like the NRFC writer come from the [Codex](https://github.com/fluidstackio/codex) marketplace:

```bash
claude plugin marketplace add fluidstackio/codex
claude plugin install codex-document-skills
```

See [Guide 02](guides/02-skills-and-mcp.md) for details.

## Contributing

1. **Guides** — Improve walkthroughs or add new ones in `guides/`
2. **Skill blueprints** — Add or improve templates in `skill-blueprints/`
3. **Integrations** — See [.marvin/integrations/CLAUDE.md](.marvin/integrations/CLAUDE.md)
4. **Bug fixes** — Submit a PR

## Resources

- [Confluence: MARVIN Guide](https://fluidstack.atlassian.net/wiki/spaces/Networking/pages/531988569)
- [Codex Skills Repo](https://github.com/fluidstackio/codex)
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)

---

Originally created by [Sterling Chin](https://sterlingchin.com). Adapted for Fluidstack Infrastructure org.

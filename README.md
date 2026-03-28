# MARVIN - Your AI Chief of Staff

**MARVIN** = Manages Appointments, Reads Various Important Notifications

An AI assistant that remembers your conversations, tracks your goals, and helps you stay organized. Like having a personal chief of staff who never forgets anything.

## Why MARVIN?

MARVIN extends Claude Code with capabilities designed for getting things done:

- **Session continuity** - Pick up where you left off, even days later. Every conversation builds on the last.
- **Goal tracking** - Set work and personal goals, MARVIN monitors progress and nudges you forward.
- **Tool integrations** - Connect to Google Workspace, Microsoft 365, Atlassian, Slack, Linear, Notion, Telegram, and more.
- **Extensibility** - Add commands, agents, and skills tailored to your workflow. Create new capabilities with simple markdown files.
- **Thought partner** - MARVIN pushes back on weak ideas, asks probing questions, and helps you think through decisions. Not just a yes-man.

## Quick Start with Claude Code

1. Clone this repository:
   ```bash
   git clone git@github.com:fluidstackio/fs-tq-marvin-template.git
   cd fs-tq-marvin-template
   ```

2. Open in Claude Code:
   ```bash
   claude
   ```

3. Ask MARVIN to help you set up:
   > "Help me set up MARVIN"

That's it. MARVIN walks you through the rest: your profile, goals, workspace location, and optional integrations.


## What You Get

### Daily Workflow

Start your day with `/start` for a briefing: priorities, deadlines, progress toward goals. Work naturally throughout the day, MARVIN remembers everything. End with `/end` to save context for next time.

Between sessions, `/update` saves progress without ending. `/sync` pulls new features from this template into your workspace.

### Commands

| Command | What It Does |
|---------|--------------|
| `/start` | Start your day with a briefing |
| `/end` | End session and save everything |
| `/update` | Quick checkpoint (save progress) |
| `/report` | Generate a weekly summary |
| `/commit` | Review and commit git changes |
| `/status` | Check integration & workspace health |
| `/sync` | Get updates from the template |
| `/help` | Show all commands and integrations |

### Integrations

MARVIN connects to tools you already use:

| Integration | What It Provides |
|-------------|------------------|
| [Google Workspace](.marvin/integrations/google-workspace/) | Gmail, Calendar, Drive |
| [Microsoft 365](.marvin/integrations/ms365/) | Outlook, Calendar, OneDrive, Teams |
| [Atlassian](.marvin/integrations/atlassian/) | Jira, Confluence |
| [Slack](.marvin/integrations/slack/) | Channel monitoring, posting |
| [Linear](.marvin/integrations/linear/) | Issue tracking |
| [Notion](.marvin/integrations/notion/) | Page reading, database queries |
| [Telegram](.marvin/integrations/telegram/) | Chat with MARVIN from your phone |
| [Parallel Search](.marvin/integrations/parallel-search/) | Web search capabilities |

Each integration includes setup instructions in its directory.

### Skills and Agents

MARVIN uses a `.claude/` directory structure for extensibility:

- **Commands** (`.claude/commands/`) - User-triggered workflows you invoke with slash commands
- **Agents** (`.claude/agents/`) - Specialized subagents MARVIN spawns for delegated work
- **Skills** (`.claude/skills/`) - Reusable capabilities Claude Code invokes contextually

Templates are included for each type. Just say "create a skill for X" and MARVIN generates the file.

## How It Works

MARVIN separates your workspace from the template:

```
~/marvin/                    Your workspace (your data lives here)
├── CLAUDE.md               Your profile and preferences
├── state/                  Your goals and priorities
├── sessions/               Your daily session logs
└── ...

~/fs-tq-marvin-template/    Template (get updates here)
├── .marvin/                Setup scripts and integrations
├── .claude/                Command and agent templates
└── ...
```

Your workspace holds all personal data. The template provides updates. Run `/sync` from your workspace to pull new features without overwriting your data.

## Migrating from Older Versions

If you were using MARVIN before the workspace separation:

```bash
cd fs-tq-marvin-template
./.marvin/migrate.sh
```

The script copies your profile, goals, sessions, reports, and custom skills to a new workspace. Nothing is deleted from your old installation. Verify the new workspace works, then clean up the old one.

## Contributing

MARVIN welcomes contributions in three areas:

1. **Integrations** - Add support for new tools. See [.marvin/integrations/CLAUDE.md](.marvin/integrations/CLAUDE.md) for patterns and security requirements.
2. **Commands, agents, skills** - Extend MARVIN's capabilities. Templates are in `.claude/commands/`, `.claude/agents/`, and `.claude/skills/`.
3. **Bug fixes** - Found an issue? Submit a PR with the fix and a test case.

Fork the repo, create a branch, and submit a PR. All contributions are reviewed.

## About

MARVIN is named after the Paranoid Android from The Hitchhiker's Guide to the Galaxy.

Originally created by [Sterling Chin](https://sterlingchin.com). Adapted for Fluidstack Infrastructure org.

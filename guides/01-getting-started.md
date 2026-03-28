---
name: guide-getting-started
description: >
  Interactive guide to install Claude Code, fork the MARVIN template, and run
  initial setup. Triggers on: "/guide getting-started",
  "help me get started", "how do I set up MARVIN".
---

# Getting Started with MARVIN

> **Reading this on GitHub?** Follow the steps below at your own pace.
> **Inside MARVIN?** Say `/guide getting-started` and I'll walk you through it.

## Prerequisites

- A Mac or Linux computer
- A terminal application (Terminal.app on Mac, or any terminal on Linux)
- GitHub access to the Fluidstack org (SSH or HTTPS)
- An Anthropic account with a Claude Pro or Team subscription

## What You'll Set Up

By the end of this guide you'll have:
- Claude Code installed on your machine
- Your own fork of the MARVIN template
- A personalized MARVIN workspace with your profile
- A `marvin` command to launch your AI Chief of Staff from anywhere

## Step 1: Install Claude Code

Claude Code is the CLI tool that powers MARVIN. Install it with one command:

**macOS (via Homebrew):**
```bash
brew install claude-code
```

**Linux (via npm):**
```bash
npm install -g @anthropic-ai/claude-code
```

Verify it installed:
```bash
claude --version
```

You should see a version number like `1.x.x`. If you get "command not found", close and reopen your terminal, then try again.

## Step 2: Verify GitHub Access

MARVIN's template lives in a private GitHub repo. Let's make sure you can access it.

**If you use SSH (most common):**
```bash
ssh -T git@github.com
```
You should see: "Hi {username}! You've successfully authenticated..."

**If you use HTTPS with a token:**
```bash
gh auth status
```
You should see your GitHub username and "Logged in to github.com".

**Don't have access?** Ask your team lead or IT to add you to the `fluidstackio` GitHub org.

## Step 3: Fork and Clone

1. **Fork the template** on GitHub: go to [github.com/fluidstackio/fs-tq-marvin-template](https://github.com/fluidstackio/fs-tq-marvin-template) and click **Fork** in the top-right corner. This creates your own copy under your GitHub account.

2. **Clone your fork:**
```bash
cd ~/git  # or wherever you keep repos
git clone git@github.com:YOUR_USERNAME/fs-tq-marvin-template.git
cd fs-tq-marvin-template
```

3. **Add the upstream remote** so you can pull template updates later:
```bash
git remote add upstream git@github.com:fluidstackio/fs-tq-marvin-template.git
```

Now `origin` points to your fork (your personal copy) and `upstream` points to the org template (where updates come from).

## Step 4: Run Setup

```bash
./.marvin/setup.sh
```

The setup script will ask you a few questions:
1. **Your name and role** — So MARVIN knows who you are.
2. **Your Infrastructure role** — Network Engineer, Program Manager, or ICT Architect. This sets sensible defaults for Jira projects, Slack channels, etc.
3. **Communication style** — How MARVIN should talk to you.
4. **Your IDE** — So the `mcode` command opens the right editor.

The script personalizes your `CLAUDE.md` and `config.yaml`, sets up a `marvin` shell command, and installs base integrations.

## Step 5: Launch MARVIN

Open a **new terminal window** (important — the shell alias needs a fresh terminal), then:

```bash
marvin
```

You should see the MARVIN ASCII art banner and Claude Code will start up.

## Step 6: Verify

Inside MARVIN, type:
```
/help
```

You should see a list of available commands (`/start`, `/end`, `/update`, etc.). If you do, you're all set.

## What's Next

Run `/guide skills-and-mcp` to install company-wide skills like the NRFC writer, or type `/start` to begin your first session.

## Keeping Updated

When new features are added to the MARVIN template, pull them into your fork:

```bash
git pull upstream main
```

Or use the `/sync` command inside MARVIN, which does this for you. See [Guide 06](06-keeping-updated.md) for details.

## Troubleshooting

**"command not found: marvin"** — Open a new terminal window. The setup added the command to your shell config, but it only takes effect in new terminals.

**"permission denied" when cloning** — Your GitHub SSH key may not be set up. Run `ssh-keygen` to create one and add it to GitHub (Settings > SSH Keys).

**Setup script fails** — Make sure you have Homebrew (Mac) or npm (Linux) installed. The script will try to install them, but if it can't, install manually first.

**Origin points to the org repo** — You cloned the org repo directly instead of forking first. Fix it:
```bash
# Rename current origin to upstream
git remote rename origin upstream
# Add your fork as origin
git remote add origin git@github.com:YOUR_USERNAME/fs-tq-marvin-template.git
git push -u origin main
```

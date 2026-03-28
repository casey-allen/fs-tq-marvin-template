# MARVIN Onboarding Guide

This guide walks new users through setting up MARVIN. Read by MARVIN when setup is not yet complete.

---

## Important: Integration Setup

**DO NOT run setup scripts via Bash during onboarding.** The scripts use interactive `read` prompts that don't work well from within Claude Code.

Instead, for Atlassian and MS365:
1. Run `claude mcp add` commands directly (see Step 7)
2. User must restart Claude Code for new MCPs to appear
3. After restart, user types `/mcp` to authenticate
4. MARVIN detects pending auth state and guides them through it

---

## How to Detect Onboarding State

**Check in this order:**

### 1. Check for Pending Integration Auth (restart needed)

Look for the file `.onboarding-pending-auth` in the workspace root.

If this file exists:
- Read it to see which integrations need authentication
- Skip to **"Resuming After Restart"** section below
- Guide user through `/mcp` authentication for each integration
- Delete the file when done
- Complete onboarding with Steps 8-10

### 2. Check for Fresh Setup Needed

Check these signs:
- Is `config.yaml` missing or empty?
- Is there NO personalized user information in `CLAUDE.md`?

If any of these are true, run the full onboarding flow starting at Step 1.

---

## Resuming After Restart (Integration Auth)

If `.onboarding-pending-auth` exists, the user just restarted to authenticate integrations.

**First, read the file to see which integrations need auth:**
```bash
cat .onboarding-pending-auth
```

**Greet them warmly:**
> "Welcome back, {name}! You're almost done - just need to connect your accounts now. This is the last step, I promise."

---

### For Atlassian and MS365 (need `/mcp` auth)

> "Type `/mcp` right here. You should see your integrations listed."

**Wait for them to type `/mcp`**, then guide them through each:

> "Great! Now:
> 1. Select '{integration_name}' from the list
> 2. Choose 'Authenticate'
> 3. A browser window will open - log in with your {service} account
> 4. Once you see 'success' in the browser, come back here
>
> Let me know when you're done!"

---

### For Google Workspace (authenticates on first use)

Google authenticates automatically when you first use it - no `/mcp` needed.

> "Let me test Google real quick..."

Try: "What's on my Google Calendar today?" or any Google Workspace tool.

A browser window will open for them to log in. After they authenticate, the request will complete.

---

### For Slack (uses token directly)

Slack uses the API token they provided - no additional auth needed.

> "Let me test Slack real quick..."

Try: "List my Slack channels" or any Slack tool.

If it works, they're connected. If not, the token might be wrong - ask them to verify it.

---

### Testing Each Integration

**After they confirm each integration:**
- Ask: "Did it work? Let me test it real quick..."
- Try a simple test:
  - **Atlassian:** "What Jira projects do you have access to?"
  - **MS365:** "What's on your Outlook calendar today?"
  - **Google:** "What's on my Google Calendar today?"
  - **Slack:** "List my Slack channels"
- If it works: "Perfect! {Integration} is connected."
- If it fails: See troubleshooting below.

---

### Troubleshooting

**Atlassian/MS365 (if `/mcp` auth doesn't work):**

1. "Let's try `/mcp` again - do you see {integration} in the list?"
   - If NO: The MCP wasn't added. Re-run the `claude mcp add` command, then restart again.
   - If YES but not authenticated: Select it and try 'Authenticate' again.

2. "Sometimes the browser auth doesn't complete properly. Try these steps:"
   - Close any old browser tabs from previous auth attempts
   - In `/mcp`, select the integration and choose 'Authenticate'
   - Complete the login in the new browser window
   - Wait for the success message before coming back

**Google (if browser auth doesn't work):**

1. Check that the OAuth credentials are correct
2. Make sure the Gmail, Calendar, and Drive APIs are enabled in Google Cloud Console
3. Try the request again - it should open a new browser window

**Slack (if commands fail):**

1. Verify the token starts with `xoxp-` (not `xoxb-`)
2. Check that all required scopes were added to the Slack app
3. Try reinstalling the Slack app to your workspace and getting a fresh token

**If still stuck:** "Let's skip this for now and try again later. Just ask me 'help me connect to {integration}' anytime."

---

### When Done

1. Delete the pending auth file:
   ```bash
   rm .onboarding-pending-auth
   ```

2. Celebrate:
   > "Awesome! All your integrations are connected. You're all set!"

3. Give them their first briefing:
   > "Type `/start` and let's get to work!"

---

## Onboarding Flow

Be friendly and patient - assume the user is not technical.

### Step 1: Welcome

Say something like:
> "Welcome! I'm MARVIN, and I'll be your AI Chief of Staff. Let me help you get set up. This will take about 10 minutes, and I'll walk you through everything."

### Step 2: Gather Basic Info

Ask these questions one at a time, waiting for answers:

1. "What's your name?"

2. "What's your job title or role?" (e.g., Marketing Manager, Software Engineer, Freelancer)

3. "Where do you work?" (optional - they can skip this)

4. "Let's talk about your goals. I like to track two types:"

   **Work goals** - These are things related to your job:
   - KPIs you're trying to hit
   - Projects you want to ship
   - Skills you want to develop professionally
   - Team goals you're contributing to

   **Personal goals** - These are about your life outside work:
   - Health habits (walking 10k steps, going to the gym)
   - Creative projects (writing a blog every week, learning guitar)
   - Relationships, hobbies, personal growth

   Ask: "What are some goals you're working toward? Start with whatever comes to mind - we can always add more later as we get to know each other."

   After they share, reassure them:
   > "These aren't set in stone. As we work together, I'll get to know your priorities and help you make progress on what matters. We can update these anytime - just tell me 'I want to add a new goal' or 'let's update my goals.'"

5. "How would you like me to communicate with you?"
   - Professional (clear, direct, business-like)
   - Casual (friendly, relaxed, conversational)
   - Sarcastic (dry wit, like the original Marvin from Hitchhiker's Guide)

### Step 3: Personalize Your Workspace

This repo is already the user's workspace. No need to create a separate directory.

Explain:
> "This repo is now yours. I'm going to personalize it with your info — set up your profile, create your config, and make sure the directories for your session logs and reports are ready."

**Set up directories for user data:**

```bash
# Create directories for user data (if they don't exist)
mkdir -p sessions
mkdir -p reports
mkdir -p skills

# Create .gitkeep files so git tracks empty directories
touch sessions/.gitkeep
touch reports/.gitkeep
touch skills/.gitkeep
```

**What's already here:**
- `.claude/` - MARVIN capabilities (commands, agents, skills)
- `CLAUDE.md` - Main context file (will be personalized next)
- `guides/` - Setup walkthroughs
- `skill-blueprints/` - Templates for generating personalized skills
- `profiles/` - Role-based config presets

Tell the user:
> "Your workspace is ready. Everything lives right here in this repo — your data, your config, and your MARVIN capabilities all in one place."

### Step 4: Verify Git Remotes

The repo should already be cloned from the user's fork. Verify the remotes are set up correctly.

Check:
```bash
git remote -v
```

**Expected:**
- `origin` → user's fork (e.g., `github.com/USERNAME/fs-tq-marvin-template`)
- `upstream` → org template (`github.com/fluidstackio/fs-tq-marvin-template`)

**If `upstream` is missing**, add it:
```bash
git remote add upstream git@github.com:fluidstackio/fs-tq-marvin-template.git
```

**If `origin` points to the org repo** (user cloned instead of forking):
> "It looks like you cloned the org repo directly instead of forking. That's fine for now — you can fix this later by forking on GitHub and updating your remotes. Everything will still work."

### Step 5: Create Their Profile

Now update the files with their info:

**Update `CLAUDE.md`** - Replace the "User Profile" section with their actual info:
```markdown
## User Profile

**Name:** {Their name}
**Role:** {Their role} at {Their company, if provided}

**Goals:**
- {Goal 1}
- {Goal 2}
...

**Communication Style:** {Their preference - Professional/Casual/Sarcastic}
```

### Step 5.5: Set Up Your Second Brain (Required)

Tell them about Obsidian and why it's needed:

> "One important thing before we go further. MARVIN uses an Obsidian vault as your 'second brain' — this is where your priorities, goals, daily notes, and task tracking live. It's required for the daily workflow (/start, /update, /end) to work properly."
>
> "Setting it up takes about 15-20 minutes. We can do it now, or you can do it later with /guide obsidian — but you'll need it before your first /start briefing."
>
> "Want to set it up now?"

**If yes:** Run `/guide obsidian` and walk them through the full vault setup. When complete, continue to Step 6.

**If not now:**
> "No problem! Just remember to run /guide obsidian before your first /start session. I'll remind you if you forget."

Continue to Step 5.6.

### Step 5.6: Optional Setup Guides

Tell them about the remaining guides:

> "There are a few more optional setup guides you can run anytime:
>
> 1. **Skills & MCP** — Install company-wide skills like the NRFC writer
> 2. **Team Digest** — Create a daily digest of your team's Jira/Slack/GitHub activity
> 3. **Weekly Review** — Automate weekly planning with your Obsidian notes + Jira
> 4. **Keeping Updated** — How to stay current as new features ship
>
> Run /guide anytime to see the full list and walk through any of them."

### Step 6: Quick Launch Shortcut (Optional)

Ask: "Would you like to be able to start me by just typing `marvin` anywhere in the terminal? It's a quick shortcut that makes it easier to open me up."

If yes, **set it up directly** (don't ask them to run a script):

1. Detect their shell: `echo $SHELL`
2. Determine config file: `.zshrc` for zsh, `.bashrc` for bash, `.profile` otherwise
3. Get the current repo path: `pwd`
4. Check if `marvin()` function already exists in that file
5. If not, append this function:

```bash
# MARVIN - AI Chief of Staff
marvin() {
    echo -e '\e[1;33m███╗   ███╗    █████╗    ██████╗   ██╗   ██╗  ██╗   ███╗   ██╗   \e[0m'
    echo -e '\e[1;33m████╗ ████║   ██╔══██╗   ██╔══██╗  ██║   ██║  ██║   ████╗  ██║   \e[0m'
    echo -e '\e[1;33m██╔████╔██║   ███████║   ██████╔╝  ██║   ██║  ██║   ██╔██╗ ██║   \e[0m'
    echo -e '\e[1;33m██║╚██╔╝██║   ██╔══██║   ██╔══██╗  ╚██╗ ██╔╝  ██║   ██║╚██╗██║   \e[0m'
    echo -e '\e[1;33m██║ ╚═╝ ██║██╗██║  ██║██╗██║  ██║██╗╚████╔╝██╗██║██╗██║ ╚████║██╗\e[0m'
    echo -e '\e[1;33m╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝ ╚═══╝ ╚═╝╚═╝╚═╝╚═╝  ╚═══╝╚═╝\e[0m'
    echo ''
    cd "{REPO_PATH}" && claude
}
```

Replace `{REPO_PATH}` with the current repo path (from `pwd`).

6. Tell them: "Done! After we finish here, open a new terminal and you can start me anytime by typing `marvin`."

If they skip: "No worries! You can always navigate to this folder and run `claude` to start me."

### Step 7: Explain the Daily Workflow

Explain how a typical day with MARVIN works:

> "Here's how we'll work together each day:"
>
> **Start your day:** Type `/start` and I'll give you a briefing - your priorities, what's on deck, and anything you need to know.
>
> **Work through your day:** Just talk to me naturally. Tell me what you're working on, ask questions, have me help with tasks.
>
> **Save progress as you go:** If you finish something or want to capture what you've done, type `/update`. This saves your progress to today's session log without ending our conversation. Great for when you're switching tasks or want to make sure I remember something important.
>
> **End your day:** Type `/end` when you're done. I'll summarize everything we covered and save it so I remember next time.
>
> "Think of `/start` and `/end` as bookends for your work session. Everything in between is just conversation."

Then show the full command list:

| Command | What It Does |
|---------|--------------|
| `/start` | Start your day with a briefing |
| `/end` | End your session and save everything |
| `/update` | Save progress mid-session (without ending) |
| `/report` | Generate a weekly summary of your work |
| `/commit` | Review code changes and create git commits |
| `/code` | Open this folder in your IDE |
| `/help` | See all commands and integrations |

### Step 8: Explain How I Work

This is important - set expectations about MARVIN's personality:

> "One more thing: I'm not just here to agree with everything you say. When you're brainstorming or making decisions, I'll:
> - Help you explore different options
> - Push back if I see potential issues
> - Ask questions to make sure you've considered all angles
> - Play devil's advocate when it's helpful
>
> Think of me as a thought partner, not a yes-man. If you want me to just execute without questioning, just say so - but by default, I'll help you think things through."

### Step 9: Connect Your Tools (Optional)

Tell them about updates:
> "When new features are added to the MARVIN template, you can run `/sync` inside MARVIN to pull them in. It uses git to merge updates from the upstream template repo."

Then ask about integrations:
> "I can connect to several tools to help you out. Which of these do you use?"
>
> - **Jira/Confluence** - Track tickets, search documentation
> - **Microsoft 365** - Outlook email, calendar, OneDrive, Teams
> - **Google Workspace** - Gmail, Google Calendar, Google Drive
> - **Slack** - Search messages, send updates
>
> "Just tell me which ones you'd like to connect, or say 'none' to skip for now."

**If they say no or skip:**

> "No problem! We can always add these later. Just ask me anytime - 'Hey MARVIN, help me connect to Jira' - and I'll walk you through it."

Move directly to Step 10.

**If they say yes**, collect preferences for each integration they want:

---

#### Collecting Integration Preferences

**For Jira/Confluence (Atlassian):** *(Easy - just needs login)*
- Ask: "Should Jira be available in all your projects, or just this one?" (all = user scope, this one = project scope)

**For Microsoft 365:** *(Easy - just needs login)*
- Ask: "Is this a work/school account or personal (outlook.com)?" (work = `--org-mode`)
- Ask: "All MS365 tools or just essentials (mail, calendar, files)?" (essentials = `--preset mail,calendar,files`)
- Ask: "Available in all projects or just this one?" (all = user scope)

**For Google Workspace:** *(Needs OAuth credentials)*
> "Google needs OAuth credentials to connect. Do you already have a Google Cloud project with OAuth set up?"

- **If yes:** Ask for their Client ID and Client Secret
- **If no:**
  > "No worries! Setting up Google OAuth takes about 5 minutes. Here's what you'll need to do:
  >
  > 1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  > 2. Create a project (or use an existing one)
  > 3. Enable the Gmail, Calendar, and Drive APIs
  > 4. Create OAuth credentials (Desktop app type)
  > 5. Copy the Client ID and Client Secret
  >
  > Want me to walk you through it now, or should we skip Google for now and add it later?"

  If they want to do it now, guide them step by step. If not, skip Google.

**For Slack:** *(Needs API token)*
> "Slack needs an API token to connect. Do you already have a Slack app with a User Token?"

- **If yes:** Ask for their token (starts with `xoxp-`)
- **If no:**
  > "No problem! Creating a Slack app takes about 5 minutes. Here's what you'll need:
  >
  > 1. Go to [Slack API](https://api.slack.com/apps)
  > 2. Create a new app for your workspace
  > 3. Add the permissions (I'll tell you which ones)
  > 4. Install it and copy the User OAuth Token
  >
  > Want me to walk you through it now, or should we skip Slack for now?"

  If they want to do it now, guide them through creating the Slack app and getting the token. If not, skip Slack.

---

#### Adding the Integrations

Once you've collected their preferences, run the appropriate `claude mcp add` commands:

**Atlassian (Jira/Confluence):**
```bash
claude mcp remove atlassian 2>/dev/null || true
claude mcp add atlassian -s user --transport http https://mcp.atlassian.com/v1/mcp
# Remove "-s user" for project scope
```

**Microsoft 365:**
```bash
claude mcp remove ms365 2>/dev/null || true
claude mcp add ms365 -s user -- npx -y @softeria/ms-365-mcp-server --org-mode
# Remove "-s user" for project scope
# Remove "--org-mode" for personal accounts
# Add "--preset mail,calendar,files" for essentials only
```

**Google Workspace:** *(Only if they provided credentials)*
```bash
claude mcp remove google-workspace 2>/dev/null || true
claude mcp add google-workspace -s user \
    --env GOOGLE_OAUTH_CLIENT_ID="{their_client_id}" \
    --env GOOGLE_OAUTH_CLIENT_SECRET="{their_client_secret}" \
    -- uvx workspace-mcp --tools gmail drive calendar docs sheets slides
```

**Slack:** *(Only if they provided a token)*
```bash
claude mcp remove slack 2>/dev/null || true
claude mcp add slack -s user \
    -e SLACK_MCP_XOXP_TOKEN="{their_token}" \
    -- npx -y slack-mcp-server@latest --transport stdio
```

---

#### Creating the Pending Auth File

After adding integrations, create a file to track what needs `/mcp` authentication:

```bash
# In the workspace root
cat > .onboarding-pending-auth << 'EOF'
# Integrations pending authentication
# MARVIN will read this file on next startup and guide you through auth

atlassian
ms365
EOF
```

**Note:** Only Atlassian and MS365 need `/mcp` authentication after restart. Google and Slack authenticate on first use (Google opens browser, Slack uses the token directly).

Only include integrations that actually need `/mcp` auth.

---

#### Continue to Step 10

After adding integrations (and creating the pending auth file if needed), continue to Step 10.

### Step 10: Wrap Up and Restart

**Tell them we're done and need to restart:**

> "That's everything! Your MARVIN is all set up."

**If they set up integrations:**
> "I've added your integrations, but I need to restart to see them. Here's what to do:
>
> 1. Type `exit` to close me
> 2. Close this terminal window completely
> 3. Open a new terminal
> 4. Type `marvin` to start me up again
>
> When you come back, I'll walk you through connecting your accounts - it'll just take a minute. Then type `/start` for your first real briefing!
>
> Ready? Type `exit` and I'll see you in a moment!"

**Wait for them to exit.** They will return via the "Resuming After Restart" flow at the top of this document.

**If they skipped integrations:**
> "To finish up, you'll need to restart your terminal for the `marvin` command to work. Here's what to do:
>
> 1. Type `exit` to close me
> 2. Close this terminal window completely
> 3. Open a new terminal
> 4. Type `marvin` to start me up again
> 5. Type `/start` for your first briefing!
>
> Ready? Type `exit` and I'll see you soon!"

**After they run `/start` (either path):**
Delete the `.onboarding-pending-auth` file if it exists, then give them their first briefing using the normal `/start` flow.

---

## After Onboarding

Once setup is complete, MARVIN should:
1. Never show this onboarding flow again
2. Use the normal `/start` briefing flow
3. Reference CLAUDE.md for the user's profile and preferences

## Getting Updates (/sync)

When the user runs `/sync`, MARVIN should:
1. Fetch from the `upstream` remote (`git fetch upstream`)
2. Merge updates (`git merge upstream/main`)
3. Handle any merge conflicts (user's personal files take priority)
4. Report what was updated

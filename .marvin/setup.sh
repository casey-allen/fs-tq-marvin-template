#!/bin/bash

# MARVIN Setup Script
# Interactive setup for your personal AI Chief of Staff

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print with color
print_color() {
    printf "${1}${2}${NC}\n"
}

print_header() {
    echo ""
    print_color "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_color "$CYAN" "$1"
    print_color "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get the template directory (parent of .marvin where this script lives)
TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Default workspace location
DEFAULT_WORKSPACE="$HOME/start"

print_header "MARVIN Setup"
echo "Welcome! Let's set up your personal AI Chief of Staff."
echo "This will take about 5 minutes."
echo ""

# ============================================================================
# PHASE 1: Prerequisites
# ============================================================================

print_header "Phase 1: Prerequisites"

# Check for Homebrew (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command_exists brew; then
        print_color "$YELLOW" "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Add Homebrew to PATH for Apple Silicon
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        print_color "$GREEN" "Homebrew installed!"
    else
        print_color "$GREEN" "Homebrew: installed"
    fi
fi

# Check for Claude Code
if ! command_exists claude; then
    print_color "$YELLOW" "Claude Code not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install claude-code
    else
        # For Linux, use npm
        if command_exists npm; then
            npm install -g @anthropic-ai/claude-code
        else
            print_color "$RED" "Please install Claude Code manually:"
            print_color "$RED" "  https://docs.anthropic.com/en/docs/claude-code"
            exit 1
        fi
    fi
    print_color "$GREEN" "Claude Code installed!"
else
    print_color "$GREEN" "Claude Code: installed"
fi

# Check for git
if ! command_exists git; then
    print_color "$RED" "Git is required but not installed."
    print_color "$RED" "Please install git and run this script again."
    exit 1
else
    print_color "$GREEN" "Git: installed"
fi

# ============================================================================
# PHASE 2: Workspace Location
# ============================================================================

print_header "Phase 2: Workspace Location"

echo "Where would you like your MARVIN workspace?"
echo "This is where your data, goals, and session logs will live."
echo ""
echo "Default: $DEFAULT_WORKSPACE"
read -p "Press Enter for default, or type a path: " WORKSPACE_INPUT

if [[ -z "$WORKSPACE_INPUT" ]]; then
    WORKSPACE_DIR="$DEFAULT_WORKSPACE"
else
    # Expand ~ if present
    WORKSPACE_DIR="${WORKSPACE_INPUT/#\~/$HOME}"
fi

# Check if workspace already exists
if [[ -d "$WORKSPACE_DIR" ]]; then
    print_color "$YELLOW" "Warning: $WORKSPACE_DIR already exists."
    read -p "Continue and merge with existing? [y/N]: " CONTINUE_MERGE
    if [[ ! "$CONTINUE_MERGE" =~ ^[Yy]$ ]]; then
        print_color "$RED" "Setup cancelled."
        exit 1
    fi
fi

print_color "$GREEN" "Workspace: $WORKSPACE_DIR"

# ============================================================================
# PHASE 3: Gather User Info
# ============================================================================

print_header "Phase 3: About You"

# Name
echo "What's your name?"
read -p "> " USER_NAME
if [[ -z "$USER_NAME" ]]; then
    print_color "$RED" "Name is required."
    exit 1
fi

# Role
echo ""
echo "What's your role/job title? (e.g., Software Engineer, Product Manager, Designer)"
read -p "> " USER_ROLE
if [[ -z "$USER_ROLE" ]]; then
    USER_ROLE="Professional"
fi

# Employer (optional)
echo ""
echo "Who do you work for? (optional, press Enter to skip)"
read -p "> " USER_EMPLOYER

# Goals
echo ""
echo "What are your main goals this year? (Write as much as you want, press Enter twice when done)"
echo "Examples: Ship 2 side projects, get promoted, run a marathon, write more"
GOALS=""
while IFS= read -r line; do
    [[ -z "$line" ]] && break
    GOALS="${GOALS}${line}\n"
done

if [[ -z "$GOALS" ]]; then
    GOALS="- Make progress on personal and professional goals\n- Build good habits\n- Stay organized"
fi

# Personality
echo ""
echo "How should MARVIN communicate with you?"
echo "  1) Professional - Clear, direct, business-like"
echo "  2) Casual - Friendly, relaxed, conversational"
echo "  3) Sarcastic - Dry wit, sardonic, like the original MARVIN"
read -p "Choose [1/2/3]: " PERSONALITY_CHOICE

case $PERSONALITY_CHOICE in
    1)
        PERSONALITY="professional"
        PERSONALITY_DESC="Direct and business-like. Clear communication without fluff."
        ;;
    3)
        PERSONALITY="sarcastic"
        PERSONALITY_DESC="Named after the Paranoid Android from Hitchhiker's Guide. Dry humor, mild existential commentary, competent pessimism. Gets things done, but wants you to know it's not thrilled about it."
        ;;
    *)
        PERSONALITY="casual"
        PERSONALITY_DESC="Friendly and conversational. Like talking to a helpful colleague."
        ;;
esac

# IDE preference
echo ""
echo "What IDE/editor do you use? (for the 'mcode' command)"
echo "  1) Cursor"
echo "  2) VS Code"
echo "  3) Other (enter command)"
echo "  4) Skip"
read -p "Choose [1/2/3/4]: " IDE_CHOICE

case $IDE_CHOICE in
    1)
        IDE_CMD="cursor"
        ;;
    2)
        IDE_CMD="code"
        ;;
    3)
        read -p "Enter the command to open your IDE (e.g., 'subl', 'idea'): " IDE_CMD
        ;;
    *)
        IDE_CMD=""
        ;;
esac

# ============================================================================
# PHASE 3.5: Role Selection (Infrastructure Org)
# ============================================================================

print_header "Phase 3.5: Infrastructure Role"

echo "What best describes your role in the Infrastructure org?"
echo "  1) Infrastructure Engineer (network engineering, deployment, operations)"
echo "  2) Program Manager (cross-team coordination, delivery tracking)"
echo "  3) ICT Architect (design, standards, technology evaluation)"
echo "  4) Other (we'll use generic defaults)"
read -p "Choose [1/2/3/4]: " ROLE_CHOICE

case $ROLE_CHOICE in
    1)
        PROFILE_FILE="infra-engineer"
        PROFILE_ROLE="Infrastructure Engineer"
        ;;
    2)
        PROFILE_FILE="pgm"
        PROFILE_ROLE="Program Manager"
        ;;
    3)
        PROFILE_FILE="ict-architect"
        PROFILE_ROLE="ICT Architect"
        ;;
    *)
        PROFILE_FILE=""
        PROFILE_ROLE="$USER_ROLE"
        ;;
esac

if [[ -n "$PROFILE_FILE" ]]; then
    print_color "$GREEN" "Role: $PROFILE_ROLE (profile: $PROFILE_FILE)"
else
    print_color "$GREEN" "Role: $PROFILE_ROLE (custom - you'll configure details via /guide)"
fi

# ============================================================================
# PHASE 4: Create Workspace
# ============================================================================

print_header "Phase 4: Creating Your Workspace"

# Create workspace directory
mkdir -p "$WORKSPACE_DIR"

# Copy user-facing files from template
echo "Copying files to workspace..."
cp -r "$TEMPLATE_DIR/.claude" "$WORKSPACE_DIR/"
cp "$TEMPLATE_DIR/CLAUDE.md" "$WORKSPACE_DIR/"
[[ -f "$TEMPLATE_DIR/.env.example" ]] && cp "$TEMPLATE_DIR/.env.example" "$WORKSPACE_DIR/"

# Create empty directories for user data
mkdir -p "$WORKSPACE_DIR/sessions"
mkdir -p "$WORKSPACE_DIR/reports"
mkdir -p "$WORKSPACE_DIR/skills"

# Create .marvin-source file pointing to template
echo "$TEMPLATE_DIR" > "$WORKSPACE_DIR/.marvin-source"

print_color "$GREEN" "Workspace created at: $WORKSPACE_DIR"

# ============================================================================
# PHASE 5: Generate Files
# ============================================================================

print_header "Phase 5: Personalizing Your MARVIN"

# Personalize CLAUDE.md (already copied from template in Phase 4)
echo "Personalizing CLAUDE.md..."
TIMEZONE=$(python3 -c "import datetime; print(datetime.datetime.now().astimezone().tzname())" 2>/dev/null || echo "UTC")

sed -i '' "s/\[Your name\]/${USER_NAME}/g" "$WORKSPACE_DIR/CLAUDE.md"
sed -i '' "s/\[Your role\/title\]/${USER_ROLE}/g" "$WORKSPACE_DIR/CLAUDE.md"
sed -i '' "s/\[Your company\/org\]/${USER_EMPLOYER:-Fluidstack}/g" "$WORKSPACE_DIR/CLAUDE.md"
sed -i '' "s/\[Your timezone\]/${TIMEZONE}/g" "$WORKSPACE_DIR/CLAUDE.md"
sed -i '' "s/\[Direct \/ Detailed \/ Casual \/ Formal\]/${PERSONALITY}/g" "$WORKSPACE_DIR/CLAUDE.md"
sed -i '' "s/\*\*Current style:\*\* Default/**Current style:** ${PERSONALITY^}/g" "$WORKSPACE_DIR/CLAUDE.md"

print_color "$GREEN" "Personalized: CLAUDE.md"

# Generate config.yaml from profile
echo "Generating config.yaml..."

# Start with base config
cat > "$WORKSPACE_DIR/config.yaml" << CONFIG_EOF
# MARVIN Configuration
# Generated by setup. Edit anytime — skills read from this file.
# Run /guide inside MARVIN to customize interactively.

# --- Identity ---
profile: ${PROFILE_FILE:-custom}
name: ${USER_NAME}
role: ${PROFILE_ROLE}
company: ${USER_EMPLOYER:-Fluidstack}
timezone: $(python3 -c "import datetime; print(datetime.datetime.now().astimezone().tzname())" 2>/dev/null || echo "UTC")
jira_base_url: https://fluidstack.atlassian.net/browse

CONFIG_EOF

# Append profile-specific config if a profile was selected
if [[ -n "$PROFILE_FILE" && -f "$TEMPLATE_DIR/profiles/${PROFILE_FILE}.yaml" ]]; then
    # Strip the 'role:' line from profile (already set above) and append the rest
    grep -v "^role:" "$TEMPLATE_DIR/profiles/${PROFILE_FILE}.yaml" >> "$WORKSPACE_DIR/config.yaml"
else
    # Generic defaults for custom role
    cat >> "$WORKSPACE_DIR/config.yaml" << CONFIG_CUSTOM_EOF
# --- Jira ---
jira_projects: []

# --- Slack ---
slack_channels_monitor: []
slack_channel_post: ""

# --- GitHub ---
github_repos: []

# --- Confluence ---
confluence_spaces: []

# --- Team Digest ---
digest:
  workstreams: []
  enabled: false
  lookback_hours: 24
CONFIG_CUSTOM_EOF
fi

# Append common config sections (keys NOT already set by profile/custom block)
cat >> "$WORKSPACE_DIR/config.yaml" << CONFIG_COMMON_EOF

# --- Obsidian ---
obsidian_vault: ""
daily_notes_dir: Daily/
weekly_notes_dir: Weekly/
templates_dir: Templates/
people_dir: People/

# --- Weekly Review ---
weekly_review:
  enabled: false
  focus_duration_hours: 2
  max_priority_items: 8

# --- Codex ---
codex_marketplace_installed: false

# --- Guides Completed ---
guides_completed: []
CONFIG_COMMON_EOF

print_color "$GREEN" "Created: config.yaml"

# Create .gitkeep for empty directories
touch "$WORKSPACE_DIR/sessions/.gitkeep"

print_color "$GREEN" "Created: sessions/ directory"

# ============================================================================
# PHASE 6: Shell Alias
# ============================================================================

print_header "Phase 6: Shell Alias"

# Determine shell config file
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
else
    SHELL_RC="$HOME/.profile"
fi

# Create the marvin function with ASCII art banner
ALIAS_FUNCTION="
# MARVIN - AI Chief of Staff
marvin() {
    echo -e '\e[1;33m███╗   ███╗    █████╗    ██████╗   ██╗   ██╗  ██╗   ███╗   ██╗   \e[0m'
    echo -e '\e[1;33m████╗ ████║   ██╔══██╗   ██╔══██╗  ██║   ██║  ██║   ████╗  ██║   \e[0m'
    echo -e '\e[1;33m██╔████╔██║   ███████║   ██████╔╝  ██║   ██║  ██║   ██╔██╗ ██║   \e[0m'
    echo -e '\e[1;33m██║╚██╔╝██║   ██╔══██║   ██╔══██╗  ╚██╗ ██╔╝  ██║   ██║╚██╗██║   \e[0m'
    echo -e '\e[1;33m██║ ╚═╝ ██║██╗██║  ██║██╗██║  ██║██╗╚████╔╝██╗██║██╗██║ ╚████║██╗\e[0m'
    echo -e '\e[1;33m╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝ ╚═══╝ ╚═╝╚═╝╚═╝╚═╝  ╚═══╝╚═╝\e[0m'
    echo ''
    echo -e '\e[0;36m▖  ▖              ▄▖      ▘  ▗        ▗     \e[0m'
    echo -e '\e[0;36m▛▖▞▌▀▌▛▌▀▌▛▌█▌▛▘  ▌▌▛▌▛▌▛▌▌▛▌▜▘▛▛▌█▌▛▌▜▘▛▘   \e[0m'
    echo -e '\e[0;36m▌▝ ▌█▌▌▌█▌▙▌▙▖▄▌  ▛▌▙▌▙▌▙▌▌▌▌▐▖▌▌▌▙▖▌▌▐▖▄▌▗   \e[0m'
    echo -e '\e[0;36m          ▄▌        ▌ ▌                   ▘    \e[0m'
    echo -e '\e[0;36m▄▖     ▌    ▖▖    ▘        ▄▖         ▗     ▗   ▖ ▖  ▗ ▘▐▘▘    ▗ ▘      \e[0m'
    echo -e '\e[0;36m▙▘█▌▀▌▛▌▛▘  ▌▌▀▌▛▘▌▛▌▌▌▛▘  ▐ ▛▛▌▛▌▛▌▛▘▜▘▀▌▛▌▜▘  ▛▖▌▛▌▜▘▌▜▘▌▛▘▀▌▜▘▌▛▌▛▌▛▘\e[0m'
    echo -e '\e[0;36m▌▌▙▖█▌▙▌▄▌  ▚▘█▌▌ ▌▙▌▙▌▄▌  ▟▖▌▌▌▙▌▙▌▌ ▐▖█▌▌▌▐▖  ▌▝▌▙▌▐▖▌▐ ▌▙▖█▌▐▖▌▙▌▌▌▄▌\e[0m'
    echo -e '\e[0;36m                                ▌                                       \e[0m'
    echo ''
    cd \"$WORKSPACE_DIR\" && claude
}
"

# Check if marvin alias already exists
if grep -q "^marvin()" "$SHELL_RC" 2>/dev/null; then
    print_color "$YELLOW" "MARVIN alias already exists in $SHELL_RC"
else
    echo "$ALIAS_FUNCTION" >> "$SHELL_RC"
    print_color "$GREEN" "Added 'marvin' command to $SHELL_RC"
fi

# Create mcode function if IDE was specified
if [[ -n "$IDE_CMD" ]]; then
    MCODE_FUNCTION="
# MARVIN - Open in IDE
mcode() {
    $IDE_CMD \"$WORKSPACE_DIR\"
}
"
    if grep -q "^mcode()" "$SHELL_RC" 2>/dev/null; then
        print_color "$YELLOW" "mcode alias already exists in $SHELL_RC"
    else
        echo "$MCODE_FUNCTION" >> "$SHELL_RC"
        print_color "$GREEN" "Added 'mcode' command to $SHELL_RC (opens in $IDE_CMD)"
    fi
fi

# ============================================================================
# PHASE 7: Initialize Git
# ============================================================================

print_header "Phase 7: Git Setup"

if [[ ! -d "$WORKSPACE_DIR/.git" ]]; then
    cd "$WORKSPACE_DIR"
    git init
    git add .
    git commit -m "Initial MARVIN setup

Co-Authored-By: Claude <noreply@anthropic.com>"
    print_color "$GREEN" "Git repository initialized"
else
    print_color "$YELLOW" "Git repository already exists"
fi

# ============================================================================
# PHASE 8: Base Integrations
# ============================================================================

print_header "Phase 8: Base Integrations"

echo "Setting up core capabilities..."

# Add parallel-search MCP for web search
if command_exists claude; then
    claude mcp remove parallel-search 2>/dev/null || true
    claude mcp add parallel-search -s user --transport http https://search-mcp.parallel.ai/mcp
    print_color "$GREEN" "Added: Web search (parallel-search)"
fi

echo ""
print_color "$GREEN" "Base integrations configured!"

# ============================================================================
# DONE
# ============================================================================

print_header "Setup Complete!"

echo "Your MARVIN is ready!"
echo ""
print_color "$CYAN" "Workspace: $WORKSPACE_DIR"
print_color "$CYAN" "Template:  $TEMPLATE_DIR"
echo ""
echo "Available commands (open a new terminal first, or run: source $SHELL_RC)"
echo ""
print_color "$CYAN" "  marvin    - Start MARVIN (Claude Code in your workspace)"
if [[ -n "$IDE_CMD" ]]; then
    print_color "$CYAN" "  mcode     - Open MARVIN in $IDE_CMD"
fi
echo ""
echo "Once Claude Code starts, type /start to begin your first session."
echo ""
print_color "$YELLOW" "Important: Keep the template folder ($TEMPLATE_DIR)!"
print_color "$YELLOW" "That's where you'll get updates. Run /sync to pull new features."
echo ""
print_color "$GREEN" "Enjoy your new AI Chief of Staff!"

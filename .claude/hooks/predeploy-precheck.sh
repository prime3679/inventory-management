#!/bin/bash

# PreToolUse hook for the Bash tool.
# Detects deploy-related commands (git push, npm run build/deploy, npm publish)
# and runs the frontend build first. If the build fails, the command is blocked.
#
# Blocking protocol: write the reason to STDERR and exit 2. Claude Code feeds
# stderr back to the model on exit code 2. (Do not mix this with a JSON
# decision on stdout — only one mechanism should be used.)
#   exit 0 = allow, exit 2 = block (reason on stderr).

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command being run
if command -v jq &> /dev/null; then
    CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
else
    CMD=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"command"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//')
fi

# Match deploy-related commands by their command token, not as a loose
# substring, so unrelated commands (e.g. `grep deploy`, `cat deploy.md`,
# `git log --grep push`) don't trigger a full build.
DEPLOY_RE='(^|[[:space:]]|;|&|\|)(git[[:space:]]+push|npm[[:space:]]+run[[:space:]]+build|npm[[:space:]]+run[[:space:]]+deploy|npm[[:space:]]+publish)([[:space:]]|;|&|\||$)'

if [[ ! "$CMD" =~ $DEPLOY_RE ]]; then
    # Not a deploy command — allow it through immediately.
    exit 0
fi

# Find the project root (where client/ directory lives)
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CLIENT_DIR="$PROJECT_ROOT/client"

# Fail open (allow) when we can't run the build, so the hook never blocks a
# legitimate push just because the environment isn't set up. It only blocks on
# an actual build failure.
if [ ! -d "$CLIENT_DIR" ]; then
    echo "predeploy-precheck: skipping build (client/ not found at $CLIENT_DIR)." >&2
    exit 0
fi

if [ ! -d "$CLIENT_DIR/node_modules" ]; then
    echo "predeploy-precheck: skipping build (dependencies not installed; run 'npm install' in client/ to enable the pre-deploy build check)." >&2
    exit 0
fi

# Run the frontend build check
BUILD_OUTPUT=$(cd "$CLIENT_DIR" && npm run build 2>&1)
BUILD_EXIT=$?

if [ $BUILD_EXIT -ne 0 ]; then
    {
        echo "Pre-deploy build check FAILED. Fix the build errors below before pushing/deploying:"
        echo
        echo "$BUILD_OUTPUT" | tail -30
    } >&2
    exit 2
fi

# Build passed — allow the command
exit 0

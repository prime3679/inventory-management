#!/bin/bash

# PreToolUse hook for Bash tool
# Detects deploy-related commands (git push, npm run build, deploy)
# and runs a frontend build check before allowing them through.
# Exit 0 = allow, Exit 2 = block with message.

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command being run
if command -v jq &> /dev/null; then
    CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
else
    CMD=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"command"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//')
fi

# Check if this is a deploy-related command
IS_DEPLOY=false
case "$CMD" in
    *"git push"*)     IS_DEPLOY=true ;;
    *"npm run build"*) IS_DEPLOY=true ;;
    *"deploy"*)       IS_DEPLOY=true ;;
    *"npm run deploy"*) IS_DEPLOY=true ;;
    *"npm publish"*)  IS_DEPLOY=true ;;
esac

# If not a deploy command, allow it through immediately
if [ "$IS_DEPLOY" = false ]; then
    exit 0
fi

# Find the project root (where client/ directory lives)
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CLIENT_DIR="$PROJECT_ROOT/client"

if [ ! -d "$CLIENT_DIR" ]; then
    echo '{"decision":"block","reason":"Pre-deploy check failed: client/ directory not found at '"$CLIENT_DIR"'. Cannot verify frontend build."}'
    exit 2
fi

# Run the frontend build check
BUILD_OUTPUT=$(cd "$CLIENT_DIR" && npm run build 2>&1)
BUILD_EXIT=$?

if [ $BUILD_EXIT -ne 0 ]; then
    # Truncate output to last 30 lines to keep the message readable
    TRIMMED=$(echo "$BUILD_OUTPUT" | tail -30)
    echo '{"decision":"block","reason":"Pre-deploy build check FAILED. Fix build errors before pushing/deploying.\n\n'"$(echo "$TRIMMED" | sed 's/"/\\"/g' | tr '\n' ' ')"'"}'
    exit 2
fi

# Build passed — allow the command
exit 0

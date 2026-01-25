#!/bin/bash
# Only run in remote (web) environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

# Install Agent OS base system
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/scripts/base-install.sh | bash

# Install into this project
~/agent-os/scripts/project-install.sh --claude-code-commands true --use-claude-code-subagents true
exit 0
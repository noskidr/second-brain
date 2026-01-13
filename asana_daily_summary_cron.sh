#!/bin/bash
# Cron wrapper for asana_daily_summary.sh
# Loads environment and runs with all options

# Load environment variables (set -a auto-exports all sourced vars)
set -a
source ~/.claude/.env 2>/dev/null || true
set +a
source ~/.zshrc 2>/dev/null || true

# Ensure PATH includes common locations
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

# Run the summary script with all options
/Users/dikson/Work/second_brain/asana_daily_summary.sh -a >> /Users/dikson/Work/second_brain/asana_daily_summary/cron.log 2>&1

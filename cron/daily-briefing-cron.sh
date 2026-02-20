#!/bin/bash
# Daily Briefing Automation - 8:00 AM Daily
# Timezone: Pacific/Auckland
# Created: February 18, 2026

# Log file
LOG_FILE="/Users/michaelnetto/.openclaw/workspace/logs/daily-briefing-$(date +%Y%m%d).log"

# Create logs directory if not exists
mkdir -p "$(dirname "$LOG_FILE")"

# Log start time
echo "$(date '+%Y-%m-%d %H:%M:%S') - Daily Briefing cron started" >> "$LOG_FILE"

# Trigger daily briefing workflow via Telegram
cd /Users/michaelnetto/.openclaw/workspace
openclaw message send \
  --channel telegram \
  --target 8253520138 \
  "Daily briefing" \
  >> "$LOG_FILE" 2>&1

# Log completion time
echo "$(date '+%Y-%m-%d %H:%M:%S') - Daily Briefing cron completed" >> "$LOG_FILE"

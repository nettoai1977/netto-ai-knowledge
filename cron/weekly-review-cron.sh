#!/bin/bash
# Weekly Review Automation - 10:00 AM Sunday
# Timezone: Pacific/Auckland
# Created: February 18, 2026

# Log file
LOG_FILE="/Users/michaelnetto/.openclaw/workspace/logs/weekly-review-$(date +%Y%m%d).log"

# Create logs directory if not exists
mkdir -p "$(dirname "$LOG_FILE")"

# Log start time
echo "$(date '+%Y-%m-%d %H:%M:%S') - Weekly Review cron started" >> "$LOG_FILE"

# Trigger weekly review workflow via Telegram
cd /Users/michaelnetto/.openclaw/workspace
openclaw message send \
  --channel telegram \
  --target 8253520138 \
  "Weekly review" \
  >> "$LOG_FILE" 2>&1

# Log completion time
echo "$(date '+%Y-%m-%d %H:%M:%S') - Weekly Review cron completed" >> "$LOG_FILE"

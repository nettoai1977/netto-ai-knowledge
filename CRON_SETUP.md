# CRON SETUP GUIDE
## Automated Workflows - Daily Briefing & Weekly Review

**Created:** February 18, 2026  
**Status:** Ready for deployment

---

## 🎯 CRON AUTOMATION OVERVIEW

### Workflows to Automate
1. **Daily Briefing** - 8:00 AM daily (Pacific/Auckland timezone)
2. **Weekly Review** - 10:00 AM Sunday (Pacific/Auckland timezone)

### Expected Benefits
- **Daily Briefing:** Saves ~90 hours/year (85% time reduction)
- **Weekly Review:** Saves ~75 hours/year (80% time reduction)
- **Total Annual Savings:** ~165 hours/year

---

## 📋 CRON JOB CONFIGURATIONS

### Cron Job 1: Daily Briefing (8:00 AM Daily)

**File:** `/Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh`

```bash
#!/bin/bash
# Daily Briefing Automation - 8:00 AM Daily
# Timezone: Pacific/Auckland

# Log file
LOG_FILE="/Users/michaelnetto/.openclaw/workspace/logs/daily-briefing-$(date +%Y%m%d).log"

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
```

**Cron Schedule:**
```cron
# Run daily at 8:00 AM (Pacific/Auckland)
0 8 * * * /bin/bash /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh
```

---

### Cron Job 2: Weekly Review (10:00 AM Sunday)

**File:** `/Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron.sh`

```bash
#!/bin/bash
# Weekly Review Automation - 10:00 AM Sunday
# Timezone: Pacific/Auckland

# Log file
LOG_FILE="/Users/michaelnetto/.openclaw/workspace/logs/weekly-review-$(date +%Y%m%d).log"

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
```

**Cron Schedule:**
```cron
# Run Sunday at 10:00 AM (Pacific/Auckland)
0 10 * * 0 /bin/bash /Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron.sh
```

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Create Cron Scripts
```bash
# Create directory for cron scripts
mkdir -p /Users/michaelnetto/.openclaw/workspace/cron
mkdir -p /Users/michaelnetto/.openclaw/workspace/logs

# Make scripts executable
chmod +x /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh
chmod +x /Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron.sh
```

### Step 2: Add Crontab Entries
```bash
# Edit crontab
crontab -e

# Add these lines:
# Daily Briefing - 8:00 AM daily
0 8 * * * /bin/bash /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh

# Weekly Review - 10:00 AM Sunday
0 10 * * 0 /bin/bash /Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron.sh
```

### Step 3: Verify Crontab
```bash
# View current crontab
crontab -l

# Expected output should include both cron jobs
```

### Step 4: Test Manual Execution (Before Cron Activation)
```bash
# Test daily briefing script manually
/bin/bash /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh

# Check log file
cat /Users/michaelnetto/.openclaw/workspace/logs/daily-briefing-$(date +%Y%m%d).log

# Test weekly review script manually
/bin/bash /Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron.sh

# Check log file
cat /Users/michaelnetto/.openclaw/workspace/logs/weekly-review-$(date +%Y%m%d).log
```

### Step 5: Monitor First Automated Runs
```bash
# Watch for log file creation after 8:00 AM of first day
ls -l /Users/michaelnetto/.openclaw/workspace/logs/

# Check daily briefing log
tail -f /Users/michaelnetto/.openclaw/workspace/logs/daily-briefing-$(date +%Y%m%d).log

# After Sunday at 10:00 AM, check weekly review log
tail -f /Users/michaelnetto/.openclaw/workspace/logs/weekly-review-$(date +%Y%m%d).log
```

---

## 🔧 TROUBLESHOOTING

### Issue: Cron job not executing

**Diagnosis:**
```bash
# Check if cron service is running
sudo service cron status  # Linux
# or
launchctl list | grep cron  # macOS

# Check cron logs
sudo grep CRON /var/log/syslog  # Linux
# or
log show --predicate 'process == "cron"'  # macOS
```

**Solutions:**
- Ensure cron service is running
- Check script permissions (must be executable)
- Verify paths in scripts are absolute
- Check log files for error messages

---

### Issue: Workflow not triggered via Telegram

**Diagnosis:**
```bash
# OpenClaw connection test
openclaw status

# Test manual message
openclaw message send \
  --channel telegram \
  --target 8253520138 \
  "Cron test message"

# Check if message appeared
```

**Solutions:**
- Ensure OpenClaw is running
- Verify Telegram connection (channel ID correct)
- Check network connectivity
- Verify target ID (8253520138) is correct

---

### Issue: Log file not created

**Diagnosis:**
```bash
# Check if logs directory exists
ls -l /Users/michaelnetto/.openclaw/workspace/logs/

# Check permissions
ls -la /Users/michaelnetto/.openclaw/workspace/logs/

# Verify script has write permission
touch /Users/michaelnetto/.openclaw/workspace/logs/test.txt
```

**Solutions:**
- Ensure logs directory exists
- Check directory permissions (user must have write access)
- Verify full path to logs directory is correct in script

---

## 📊 LOG FILE FORMAT

### Daily Briefing Log Example
```
2026-02-24 08:00:00 - Daily Briefing cron started
2026-02-24 08:00:05 - Daily Briefing cron completed
```

**Expected Time:** ~5 seconds for trigger + workflow execution time (~5 minutes)

### Weekly Review Log Example
```
2026-03-02 10:00:00 - Weekly Review cron started
2026-03-02 10:00:05 - Weekly Review cron completed
```

**Expected Time:** ~5 seconds for trigger + workflow execution time (~15 minutes)

---

## 🎯 TESTING CHECKLIST

### Before Production Deployment:
- [ ] Cron scripts created and made executable
- [ ] Log directories created
- [ ] Manual script execution tested (both scripts)
- [ ] Log files created and reviewed
- [ ] Telegram message delivery verified
- [ ] Crontab entries added
- [ ] Crontab verified with `crontab -l`
- [ ] Timezone confirmed (Pacific/Auckland)
- [ ] Schedule confirmed (8:00 AM daily, 10:00 AM Sunday)

### After Production Deployment:
- [ ] First automated daily briefing observed
- [ ] Daily briefing log file reviewed
- [ ] Workflow execution logged
- [ ] First automated weekly review observed (after Sunday)
- [ ] Weekly review log file reviewed
- [ ] Workflow execution logged

---

## ⚠️ IMPORTANT NOTES

### Timezone Consideration
- **Current Timezone:** Pacific/Auckland (GMT+13)
- **Timezone offset may affect actual execution time**
- Confirm system timezone before deploying

### Manual Override
- **Manual trigger still works:**
  - Send message "Daily briefing" or "Weekly review" to 8253520138
  - Agent will execute workflow regardless of cron
- **Cron does not prevent manual execution**

### Logging Retention
- **Log files accumulate over time**
- Consider log rotation (keep last 7 days):
  ```bash
  # Add to crontab for log cleanup (runs weekly)
  0 2 * * 1 find /Users/michaelnetto/.openclaw/workspace/logs/ -name "*.log" -mtime +7 -delete
  ```

---

## ✅ DEPLOYMENT STATUS

**Pre-Deployment:**
- [ ] Scripts created and tested manually
- [ ] Log directories created
- [ ] Telegram messaging verified
- [ ] Crontab entries not yet added

**Ready for Deployment:** ✅  
**Target Deployment Date:** February 24, 2026 (Week 3 Day 1)

---

**Cron Setup Guide Complete: February 18, 2026 1:30 PM**  
**Status:** Ready for deployment  
**Next Step:** Manual testing before cron activation

---

*Cron Setup Guide Created: 2026-02-18 1:30 PM*
# CRON MANUAL TEST CHECKLIST
## Manual Testing Before Deployment

**Date:** March 3, 2026  
**Day:** 1 (of 5 in Week 4)  
**Status:** Ready for Manual Testing

---

## 🎯 TEST OBJECTIVES

**Objective:** Validate cron automation scripts work correctly before adding to crontab

**Criteria:**
- Scripts execute without errors
- Log files created properly
- Telegram messages delivered
- Workflows triggered successfully
- Execution completes without blocking

---

## 📋 PRE-TEST CHECKLIST

### Before Starting Tests

**1. Verify Scripts Exist and Executable**
[x] Check daily-briefing-cron.sh exists
[x] Check weekly-review-cron.sh exists
[x] Check permissions are executable (chmod +x already applied)
[x] Verify logs directory structure

### 2. Current Status
```
Scripts: ✅ Both cron scripts created and executable
Permissions: ✅ Both scripts have execute permissions
Directory: logs/ existing (will create files automatically)
```

---

## 🧪 TEST 1: Manual Test - Daily Briefing Cron Script

**Command to Run:**
```bash
/bin/bash /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh
```

**Expected Behavior:**
1. Creates log file: `/Users/michaelnetto/.openclaw/workspace/logs/daily-briefing-20260303.log`
2. Logs start time
3. Sends "Daily briefing" message to Telegram (target: 8253520138)
4. Logs completion time

**Expected Output:**
- Log file created with timestamps
- Telegram message appears (8253520138 receives "Daily briefing")
- Workflow executes in response (6-step daily briefing process)
- Log file updated with completion time

**Expected Execution Time:** ~5-10 seconds (trigger + workflow execution)

**How to Verify:**
```bash
# Check log file after execution (or during if verbose)
tail -f /Users/michaelnetto/.openclaw/workspace/logs/daily-briefing-20260303.log
```

**Note:** This test will actually send "Daily briefing" message to Telegram. The recipient (you) should trigger the workflow manually via message.

---

## 🧪 TEST 2: Manual Test - Weekly Review Cron Script

**Command to Run:**
```bash
/bin/bash /Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron.sh
```

**Expected Behavior:**
1. Creates log file: `/Users/michaelnetto/.openclaw/workspace/logs/weekly-review-20260303.log`
2. Logs start time
3. Sends "Weekly review" message to Telegram (target: 8253520138)
4. Logs completion time

**Expected Output:**
- Log file created with timestamps
- Telegram message appears (8253520138 receives "Weekly review")
- Workflow executes in response (4-step bilingual process)
- Log file updated with completion time

**Expected Execution Time:** ~10-15 minutes (weekly review longer than daily)

**How to Verify:**
```bash
# Check log file after execution
tail -f /Users/michaelnetto/.openclaw/workspace/logs/weekly-review-20260303.log
```

**Note:** This test will actually send "Weekly review" message to Telegram. The recipient (you) should trigger the workflow manually via message.

---

## 📋 TEST CHECKLIST (During Manual Execution)

### Daily Briefing Test

**Test Run Status:** [ ] Pending manual execution

**Checklist:**
- [ ] Script executes without errors
- [ ] Log file created in logs/ directory
- [ ] Log contains timestamps (start and completion)
- [ ] Telegram message received ("Daily briefing")
- [ ] Workflow triggers (6-step process executes)
- [ ] Workflow completes successfully

**Success Criteria ✅**
- All checklist items checked
- Execution time <10 seconds for trigger
- Log file includes both start and completion timestamps
- Workflow execution completes with 100% steps

---

### Weekly Review Test

**Test Run Status:** [ ] Pending manual execution

**Checklist:**
- [ ] Script executes without errors
- [ ] Log file created in logs/ directory
- [ ] Log contains timestamps (start and end)
- [ ] Telegram message received ("Weekly review")
- [ ] Workflow triggers (4-step bilingual process executes)
- [ ] Workflow completes with 100% accuracy

**Success Criteria ✅**
- All checklist items checked
- Execution time <20 minutes for trigger
- Log file includes both start and end timestamps
- Workflow execution completes with 100% accuracy + bilingual support

---

## ✅ AFTER TESTING: CRONTAB DEPLOYMENT

### Condition for Deployment: BOTH TESTS MUST PASS

**Deployment Criteria:**
- ✅ Daily briefing test passed (all checklist items)
- ✅ Weekly review test passed (all checklist items)
- ✅ No errors encountered during execution
- ✅ Workflow execution confirmed (100% steps, quality maintained)

---

## 🚀 CRONTAB ENTRIES TO ADD

### If Tests Pass

Add these lines via `crontab -e` (edit crontab):

```cron
# Daily Briefing - 8:00 AM Daily (Pacific/Auckland)
0 8 * * * /bin/bash /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh

# Weekly Review - 10:00 AM Sunday (Pacific/Auckland)
0 10 * * 0 /bin/bash /Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron.sh
```

### Deployment Steps

**1. Edit Crontab:**
```bash
crontab -e
```

**2. Add Lines (above) to end of file**

**3. Save and Exit**
- In vi or nano: Press ESC, type `:wq` and press Enter

**4. Verify Crontab:**
```bash
crontab -l
```

Expected Output (should include both cron jobs):
```
# m h  dom mon dow command
0 8 * * * /bin/bash /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh
0 10 * * 0 /bin/bash /Users/michaelnetto/.openclaw/workspace/weekly-review-cron.sh
```

---

## 📊 FIRST AUTOMATED RUNS

### Expected Trigger Times (Pacific/Auckland Timezone)

**Daily Briefing:**
**Next Trigger:** 8:00 AM March 4, 2026 (tomorrow at 8 AM if deployed now)
**Subsequent:** Every day at 8:00 AM

**Weekly Review:**
**Next Trigger:** 10:00 AM March 8, 2026 (next Sunday)
**Subsequent:** Every Sunday at 10:00 AM

### Monitoring First Runs

**Daily Briefing (8:00 AM):**
1. Wait until ~8:05 AM (5-10 min for execution)
2. Check log file: tail -f /Users/michaelnetto/.openclaw/workspace/logs/daily-briefing-20260304.log
3. Verify message received (check Telegram)

**Weekly Review (Sunday 10:00 AM):**
1. Wait until ~10:15 AM (10-15 min for execution)
2. Check log file: tail -f /Users/michaelnetto/.openclaw/workspace/logs/weekly-review-20260308.log
3. Verify message received (check Telegram)

---

## 🔥 TROUBLESHOOTING

### Issue: Script Doesn't Execute

**Symptoms:**
- `Permission denied` error
- `command not found` error
- No log file created

**Triage:**
```bash
# Check file exists
ls -la /Users/michaelnetto/.openclaw/workspace/cron/

# Check permissions
ls -la /Users/michaelnetto/.openclaw/workspace/cron/*.sh

# If not executable, re-add permissions
chmod +x /Users/michaelnetto/.openclaw/workspace/cron/daily-briefing-cron.sh
chmod +x /Users/michaelnetto/.openclaw/workspace/cron/weekly-review-cron-cron.sh
```

---

### Issue: Telegram Message Not Received

**Symptoms:**
- Script executes successfully
- Log file created
- No message appears in Telegram

**Triage:**
```bash
# Check OpenClaw connection
openclaw status

# Test manual message
openclaw message send \
  --channel telegram \
  --target 8253520138 \
  "Cron check: Testing openclaw connection"
```

---

### Issue: Workflow Doesn't Trigger

**Symptoms:**
- Telegram message received ("Daily briefing" or "Weekly review")
- No workflow response from agent

**Triage:**
- Check if agent is available
- Check workspace context
- Verify workflow files (DAILY_BRIEFING_WORKFLOW.md, WEEKLY_REVIEW_WORKFLOW.md) exist

---

## 📊 CRON DEPLOYMENT STATUS

### Phase Status: Manual Testing ⏳

**Preparation:** ✅ COMPLETE  
**Scripts:** ✅ READY  
**Testing:** ⏳ PENDING (Manual execution required)  
**Deployment:** ⏳ AFTER MANUAL TESTS  
**Verification:** ⏳ AFTER DEPLOYMENT

---

**Cron Manual Test Checklist Created: 2026-03-03 1:50 PM**  
**Status:** 📋 READY FOR MANUAL TESTING  
**Next:** Execute manual tests (Task 1, Task 2)  
**Deployment Pending:** Pending successful manual tests

**IMPORTANT:** These tests will actually send real messages to Telegram and trigger workflows. Execute tests only when ready to receive workflow results.

---

*Manual Test Checklist Complete* ✅  
*Next: Manual Execution (or user-decision to defer)*
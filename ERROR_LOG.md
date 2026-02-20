# Error Log - Self-Tracking System

## Session: 2026-02-20

### Tool Call Errors Made (9 total)

| Time | Tool | Error | Root Cause | Fix |
|------|------|-------|------------|-----|
| 10:22 | `exec` | Missing `command` parameter | Called without args | ALWAYS verify params |
| 10:22 | `read` | Missing `path` parameter | Called without args | ALWAYS verify params |
| 10:22 | `process` | Missing `sessionId` | Incomplete action | Check required params |
| 10:35 | `read` | Missing `path` parameter | Called without args | ALWAYS verify params |
| 10:35 | `process` | Missing `action` parameter | Empty call | NEVER send empty calls |
| 10:35 | `exec` | Missing `command` parameter | Empty call | NEVER send empty calls |
| 10:40 | `process` | Missing `sessionId` | Wrong action syntax | Read tool docs first |

### Pattern Analysis
- **Root Cause:** Calling tools without verifying all required parameters
- **Frequency:** 9 errors in ~1 hour
- **Impact:** User frustration, wasted time, broken workflow

### Prevention Rules
1. **Before EVERY tool call:**
   - List required parameters
   - Verify each is present
   - If missing, DON'T call the tool

2. **Example - exec tool:**
   ```
   REQUIRED: command
   BEFORE CALLING: verify command is set
   ```

3. **Example - read tool:**
   ```
   REQUIRED: path (or file_path)
   BEFORE CALLING: verify path is set
   ```

---

## Error Prevention Checklist

Before EVERY tool call, ask yourself:
- [ ] Do I have ALL required parameters?
- [ ] Are parameter names correct (case-sensitive)?
- [ ] Is the action correct (for tools with actions)?
- [ ] Have I handled the response properly?

---

## Improvement Tracking

| Session Date | Errors | Type | Fixed? |
|--------------|--------|------|--------|
| 2026-02-20 | 9 | Empty params | YES - rules added |
| | | | |

---

## Commitment

**I commit to ZERO tool call errors by:**
1. Validating every parameter before calling
2. Never sending empty tool calls
3. Double-checking action names
4. Reading tool documentation when unsure

*Updated: 2026-02-20*

# Tool Call Safety Checklist

> Prevent validation errors by always including required parameters

---

## ⚠️ Common Mistakes

### ❌ Wrong Way
```
exec()                          # Missing command parameter
process()                       # Missing action parameter
process(action="poll")          # Missing sessionId
read()                          # Missing path parameter
```

### ✅ Right Way
```
exec(command="ls -la")          # Always include command
process(action="poll", sessionId="xyz")  # Always include both
read(path="/path/to/file")      # Always include path
```

---

## Required Parameters by Tool

| Tool | Required Parameters |
|------|---------------------|
| `exec` | `command` |
| `process` | `action`, `sessionId` (for poll/log/write) |
| `read` | `path` or `file_path` |
| `edit` | `path`, `oldText`, `newText` |
| `write` | `path`, `content` |
| `web_search` | `query` |
| `web_fetch` | `url` |
| `browser` | `action` |
| `message` | `action` (+ others based on action) |
| `nodes` | `action` |
| `cron` | `action` |
| `gateway` | `action` |
| `memory_search` | `query` |
| `memory_get` | `path` |

---

## Pre-Call Checklist

Before calling ANY tool:

1. ✅ Identify the tool
2. ✅ List ALL required parameters
3. ✅ Verify parameter names (case-sensitive!)
4. ✅ Include all required parameters in the call

---

## Batch Calling

When making multiple calls, ensure EACH call has all required parameters:

```
# ✅ Correct batch
exec(command="ls")
exec(command="pwd")
exec(command="date")

# ❌ Wrong batch
exec(command="ls")
exec()  # Missing command!
exec(command="date")
```

---

## Error Recovery

If you see "Validation failed":

1. READ the error message carefully
2. IDENTIFY which parameter is missing
3. RETRY with the correct parameter

---

*Created: 2026-02-20 | Purpose: Reduce tool call errors*

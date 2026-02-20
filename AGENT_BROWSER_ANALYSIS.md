# Agent-Browser Analysis
## Source: Vercel Labs (https://github.com/vercel-labs/agent-browser)
**Skill:** agent-browser - Browser automation CLI for AI agents

---

## 🎯 What is Agent-Browser?

A browser automation CLI tool that enables AI agents to programmatically interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, and automating any browser task.

---

## 🌐 Core Capabilities

### 1. Browser Automation Workflow
```
1. Navigate: agent-browser open <url>
2. Snapshot: agent-browser snapshot -i (get element refs like @e1, @e2)
3. Interact: Use refs to click, fill, select
4. Re-snapshot: Fresh refs after DOM changes
```

### 2. Essential Commands

| Command | Purpose | Example |
|---------|---------|---------|
| **Navigation** | | |
| `open <url>` | Navigate to page | `agent-browser open https://example.com/form` |
| `close` | Close browser | `agent-browser close` |
| **Snapshot** | | |
| `snapshot -i` | Get interactive elements | Output: `@e1 [input email], @e2 [button] "Submit"` |
| `snapshot -i -C` | Include cursor-interactive elements | Divs with onclick, cursor:pointer |
| `snapshot -s "#selector"` | Scope to CSS selector | Focus on specific section |
| **Interaction** | | |
| `click @e1` | Click element | `agent-browser click @e2` |
| `fill @e1 "text"` | Clear and type text | `agent-browser fill @e1 "user@example.com"` |
| `type @e1 "text"` | Type without clearing | Append text |
| `select @e1 "option"` | Select dropdown option | `agent-browser select @e1 "California"` |
| `check @e1` | Check checkbox | `agent-browser check @e4` |
| `press Enter` | Press key | `agent-browser press Enter` |
| `scroll down 500` | Scroll page | `agent-browser scroll down 500` |
| **Information** | | |
| `get text @e1` | Get element text | `agent-browser get text @e1` |
| `get url` | Get current URL | `agent-browser get url` |
| `get title` | Get page title | `agent-browser get title` |
| **Wait** | | |
| `wait @e1` | Wait for element | `agent-browser wait @e1` |
| `wait --load networkidle` | Wait for page load | For slow pages |
| `wait --url "**/page"` | Wait for URL pattern | For redirects |
| `wait 2000` | Wait milliseconds | Fixed duration |
| **Capture** | | |
| `screenshot` | Screenshot to temp dir | `agent-browser screenshot` |
| `screenshot --full` | Full page screenshot | `agent-browser screenshot --full` |
| `pdf output.pdf` | Save as PDF | `agent-browser pdf output.pdf` |

---

## 🚀 Advanced Features

### 1. Session Persistence
```bash
# Save login state
agent-browser state save auth.json

# Reuse in future sessions
agent-browser state load auth.json
```

### 2. Parallel Sessions
```bash
agent-browser --session site1 open site-a.com
agent-browser --session site2 open site-b.com
agent-browser session list
```

### 3. Mobile Testing (iOS Safari)
```bash
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1  # Tap (alias for click)
agent-browser -p ios swipe up  # Mobile-specific gesture
```

### 4. Visual Browser (Debugging)
```bash
agent-browser --headed open https://example.com  # Visual browser
agent-browser highlight @e1  # Highlight element
agent-browser record start demo.webm  # Record session
agent-browser profiler start  # Chrome DevTools profiling
agent-browser profiler stop trace.json  # Save profile
```

### 5. Local Files (PDFs, HTML)
```bash
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

### 6. JSON Output for Parsing
```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

---

## 🌍 Use Cases for Your Agent Army

### 1. Automated Testing
- End-to-end web app testing
- Regression testing across browsers
- Mobile app testing (iOS Safari)

### 2. Form Automation
- Auto-fill registration forms
- Bulk data entry
- Account creation automation
- Multi-step form submission

### 3. Data Extraction
- Scrape web pages systematically
- Extract structured data from tables, lists
- Monitor competitor websites
- Collect product information

### 4. Content Monitoring
- Track website changes
- Monitor prices/products
- Check availability/status
- Document website state changes

### 5. Research & Analysis
- Automated research tasks
- Collect data from multiple sources
- Screenshot documentation
- Analyze competitor strategies

### 6. Authentication Testing
- Test login flows
- OAuth validation
- 2FA handling
- Session state validation

---

## 📊 Current Tool Stack vs agent-browser

| Aspect | Current (browser control) | agent-browser |
|--------|-------------------------|---------------|
| **Browser-based** | Basic screenshot capture | Full Playwright automation |
| **Screenshot capture** | ✅ Available | ✅ Enhanced (full page, visual mode) |
| **Form interaction** | Possible | ✅ Optimized (snapshot + ref workflow) |
| **Session persistence** | Limited | ✅ State save/load, encryption |
| **Mobile testing** | Not available | ✅ iOS Safari support |
| **Parallel sessions** | Not available | ✅ Multi-session support |
| **Video recording** | Not available | ✅ Screen recording (WebM) |
| **Profiling** | Not available | ✅ Chrome DevTools profiling |
| **Ref-based interaction** | Not available | ✅ @e1, @e2 element references |
| **Configuration file** | Not available | ✅ agent-browser.json config |
| **Template library** | Not available | ✅ Ready-to-use templates |

---

## 💡 Integration Value for Your Agent Army

**HIGH VALUE** - Adds powerful web interaction capabilities to your agents

### Immediate Benefits

1. **Form Automation** - Auto-fill, bulk data entry, save time
2. **Testing** - End-to-end web app validation, catch regressions
3. **Scraping** - Systematic data extraction, structured output
4. **Monitoring** - Track changes, prices, availability proactively

### Strategic Benefits

1. **Expansion** - From text-only to full web interaction
2. **Real-world Testing** - Test actual websites (not just APIs)
3. **Mobile Testing** - iOS Safari support (future mobile agent capabilities)
4. **Debugging** - Visual browser + video recording for analysis

### Capability Gaps Filled

- **Browser Interaction** - Your army had limited web interaction capability
- **Form Automation** - Bulk data entry now possible via agents
- **Web Testing** - Automated testing now available
- **Mobile Support** - iOS testing now possible (with Xcode + Appium)

---

## 🔧 Technical Details

### Powered by Playwright

**Browsers Supported:**
- Chromium
- Firefox
- WebKit

**Modes:**
- Headless (default) - No UI, faster
- Headed (--headed flag) - Visual debugging

**Cross-Platform:**
- macOS ✅
- Linux ✅
- Windows ✅

### Timeouts

- Default: 60 seconds for local browsers
- Slow pages: Use `wait --load networkidle`
- Dynamic content: Wait for specific element

### Ref Lifecycle (Critical)

Refs (`@e1`, `@e2`, etc.) are invalidated when page changes. Always re-snapshot after:

- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading (dropdowns, modals)

**Example:**
```bash
agent-browser click @e5  # Navigates
agent-browser snapshot -i  # MUST re-snapshot
agent-browser click @e1  # Use new refs
```

---

## ⚡ Quick Start

### Installation

```bash
npm install -g agent-browser
```

### Basic Usage

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser screenshot
agent-browser close
```

---

## 📝 Common Patterns

### Form Submission

```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe"
agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser check @e4
agent-browser click @e5
agent-browser wait --load networkidle
```

### Authentication with State Persistence

```bash
# Login once and save state
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Reuse in future sessions
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### Data Extraction

```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5  # Get specific element text
agent-browser get text body > page.txt  # Get all page text

# JSON output
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

---

## 🔧 Configuration

### Configuration File

Create `agent-browser.json` in project root:

```json
{
  "headed": true,
  "proxy": "http://localhost:8080",
  "profile": "./browser-data"
}
```

### Priority

Lowest to highest: `~/.agent-browser/config.json` < `./agent-browser.json` < env vars < CLI flags

---

## 📊 Requirements

**Basic:**
- Node.js (npm install -g agent-browser)

**Optional (Advanced):**
- Chrome remote debugging (for advanced features)
- Xcode + Appium (for iOS testing)

**No API keys required** - Uses browser automation directly

---

## ⚠️ Constraints & Limitations

### System Requirements
- Node.js environment (npm)
- Requires browser installation (Chromium included with Playwright)

### API Dependencies
- No external API keys needed
- Uses only browser automation (Playwright)

### Platform Support
- macOS, Linux, Windows (but iOS testing requires macOS + Xcode)

---

## 🚀 Integration Options

### Option A: Create Integration Skill (Recommended)
- Create `/skills/agent-browser-integration/SKILL.md`
- Add commands to your OpenClaw/Nanobot skills
- Enable agents to use browser automation
- **Time:** 2-3 hours

### Option B: Add to Workflows (Medium)
- Integrate into daily/weekly workflows for monitoring
- Automate periodic website checks
- **Time:** 1-2 hours

### Option C: Document and Evaluate (Low Priority)
- Track for future use
- Return to Week 5 deployment
- **Time:** 10 minutes

---

## 🎯 Similarity to Other Integration Tools

| Tool | Type | Purpose | Status |
|------|------|---------|--------|
| **ClawWork** | Economic benchmarking | Agent productivity measurement | TODO Task #6 (template ready) |
| **Self-Organizing Memory** | Memory enhancement | Long-term reasoning | ✅ COMPLETE (Task #7) |
| **agent-browser** | Web interaction | Browser automation | NEW (this document) |

**Pattern:** All three are integration-enhancement tools that add capabilities without replacing core agent structure.

---

## 💡 Recommendations

### For Your Agent Army

**High Priority Integration:**

1. **Form Automation** - Your agents can now fill forms automatically
2. **Testing** - Automated web app testing capability
3. **Monitoring** - Track website changes proactively

**Use Cases:**

1. **Research Agents** - Scrape data, collect information
2. **Testing Agents** - Validate web applications
3. **Monitoring Agents** - Track prices, changes, availability

---

## 📚 Documentation References

**Full Documentation:**
https://github.com/vercel-labs/agent-browser

**Deep-Dive Documentation:**
- commands.md - Full command reference
- snapshot-refs.md - Ref lifecycle, invalidation rules
- session-management.md - Parallel sessions, state persistence
- authentication.md - Login flows, OAuth, 2FA handling
- video-recording.md - Recording workflows
- profiling.md - Chrome DevTools profiling

**Templates:**
- form-automation.sh - Form filling with validation
- authenticated-session.sh - Login once, reuse state
- capture-workflow.sh - Content extraction with screenshots

---

## 🔍 Next Steps

**Integration Options:**

1. **Create Integration Skill** (Recommended - HIGH VALUE)
   - Add to skills directory
   - Enable browser automation for agents
   - Expand agent capabilities to web interaction

2. **Add to Workflows** (MEDIUM VALUE)
   - Integrate into daily/weekly monitoring
   - Automate periodic website checks

3. **Document for Future** (LOW PRIORITY)
   - Track as Task #8 in TODO.md
   - Focus on current Week 5 deployment

---

**Analysis Complete: February 18, 2026**

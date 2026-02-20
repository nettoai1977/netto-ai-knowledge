# Cloudflare + Mistral La Plateforme Integration Guide
## Task #5: Integrate Free API Providers
**Created:** February 18, 2026
**Priority:** HIGH
**Estimated Savings:** ~$550/month capacity at zero cost

---

## 📋 Integration Overview

### Providers to Add

**1. Cloudflare Workers AI**
- Base URL: `https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/v1`
- Requires: Account ID + API Token
- Limits: 10,000 neurons/day FREE
- Key Models:
  - `@cf/openai/gpt-oss-120b` - Strong reasoning (production-grade)
  - `@cf/openai/gpt-oss-20b` - Fast
  - `@cf/meta/llama-3.1-8b-instruct` - General purpose
  - `@cf/qwen/qwen3-30b-a3b-fp8` - Chinese/English
  - `@cf/deepseek-ai/deepseek-r1-distill-32b` - Reasoning

**2. Mistral La Plateforme**
- Base URL: `https://api.mistral.ai/v1`
- Requires: API Key
- Limits: 1 request/second, 500K tokens/minute, 1,000,000,000 tokens/month
- Key Models:
  - `open-mistral-7b` - Small model, fast (free tier)
  - `mistral-tiny` - Tiny model, very fast (free tier)
  - `mistral-small` - Small model, balanced (free tier)
  - `mistral-medium` - Medium model, higher performance (free tier)
  - `codestral` - Code generation specialist (free tier)

---

## 🔑 Required Setup

### Step 1: Get Cloudflare API Credentials

1. **Sign up for Cloudflare:** https://dash.cloudflare.com/sign-up
2. **Get Account ID:**
   - Log in to Cloudflare Dashboard
   - Account ID is visible in the right sidebar or in URL: `https://dash.cloudflare.com/{ACCOUNT_ID}/`
3. **Create API Token:**
   - Go to: https://dash.cloudflare.com/profile/api-tokens
   - Click "Create Token"
   - Use "Edit Cloudflare Workers" template
   - Permissions needed: Account - Workers AI Scripts - Edit
   - Account resources: Include - All accounts (or specific account)
   - Click "Continue to summary" → "Create Token"
   - **Copy the token** (you won't see it again!)

### Step 2: Get Mistral API Key

1. **Sign up for Mistral:** https://console.mistral.ai/
2. **Create API Key:**
   - Go to: https://console.mistral.ai/api-keys
   - Click "Create new key"
   - Give it a name (e.g., "OpenClaw Agent Army")
   - Copy the API key

---

## ⚙️ Configuration: Add to openclaw.json

### Current openclaw.json Structure

The providers section is in `/Users/michaelnetto/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "nvidia": { ... },
      "groq": { ... },
      "openrouter": { ... }
    }
  }
}
```

### Add Cloudflare Provider

```json
"cloudflare": {
  "baseUrl": "https://api.cloudflare.com/client/v4/accounts/{YOUR_ACCOUNT_ID}/ai/v1",
  "apiKey": "{YOUR_CLOUDFLARE_API_TOKEN}",
  "api": "openai-completions",
  "models": [
    {
      "id": "@cf/openai/gpt-oss-120b",
      "name": "GPT-OSS 120B (Cloudflare)",
      "api": "openai-completions",
      "reasoning": true,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 128000,
      "maxTokens": 4096
    },
    {
      "id": "@cf/openai/gpt-oss-20b",
      "name": "GPT-OSS 20B (Cloudflare)",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 128000,
      "maxTokens": 4096
    },
    {
      "id": "@cf/meta/llama-3.1-8b-instruct",
      "name": "LLaMA 3.1 8B Instruct (Cloudflare)",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 128000,
      "maxTokens": 4096
    },
    {
      "id": "@cf/deepseek-ai/deepseek-r1-distill-32b",
      "name": "DeepSeek R1 Distill 32B (Cloudflare)",
      "api": "openai-completions",
      "reasoning": true,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 128000,
      "maxTokens": 4096
    }
  ]
}
```

### Add Mistral Provider

```json
"mistral": {
  "baseUrl": "https://api.mistral.ai/v1",
  "apiKey": "{YOUR_MISTRAL_API_KEY}",
  "api": "openai-completions",
  "models": [
    {
      "id": "open-mistral-7b",
      "name": "Mistral 7B Open",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 32768,
      "maxTokens": 8192
    },
    {
      "id": "mistral-tiny",
      "name": "Mistral Tiny",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 32768,
      "maxTokens": 8192
    },
    {
      "id": "mistral-small",
      "name": "Mistral Small",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 32768,
      "maxTokens": 8192
    },
    {
      "id": "mistral-medium",
      "name": "Mistral Medium",
      "api": "openai-completions",
      "reasoning": true,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 32768,
      "maxTokens": 8192
    },
    {
      "id": "codestral",
      "name": "Codestral",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 32768,
      "maxTokens": 8192
    }
  ]
}
```

---

## 🧪 Testing Integration

### Test Cloudflare Workers AI

```bash
# Test GPT-OSS 120B
curl --request POST \
  --url https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/v1/chat/completions \
  --header "Authorization: Bearer {CLOUDFLARE_API_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "@cf/openai/gpt-oss-120b",
    "messages": [
      {
        "role": "user",
        "content": "What is 2+2? Answer in one word."
      }
    ]
  }'
```

### Test Mistral La Plateforme

```bash
# Test Mistral Tiny
curl --request POST \
  --url https://api.mistral.ai/v1/chat/completions \
  --header "Authorization: Bearer {MISTRAL_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "mistral-tiny",
    "messages": [
      {
        "role": "user",
        "content": "What is 2+2? Answer in one word."
      }
    ]
  }'
```

---

## 📊 Load Balancing Update (After Integration)

### Updated Priority Queue

**Priority 1: FREE Fast Tasks**
- Flash (existing)
- Groq: Llama 3.1 8B (14,400 requests/day)
- Cloudflare: GPT-OSS 20B (fast) 🆕

**Priority 2: FREE Reasoning Tasks**
- Atlas/Zen: NVIDIA GLM 4.7
- Backup: OpenRouter GPT-OSS 120B
- Fallback: Cloudflare GPT-OSS 120B 🆕
- Mistral Medium (reasoning) 🆕

**Priority 3: FREE High-Volume Processing**
- Large tasks: Mistral La Plateforme (1B tokens/month) 🆕
- Massive tasks: NVIDIA MiniMax M2.1 (1M context)

**Priority 4: FREE Vision/Multimodal**
- Vision: Groq Llama 4 Scout

### Updated Agent Assignments

**New agent roles can leverage new providers:**
- Create "MISTRAL_CODER" - Use Codestral for code generation
- Create "CLOUDFALL_BACKUP" - Use GPT-OSS 120B for backup reasoning
- Create "MISTRAL_TINY" - For ultra-fast small tasks

---

## 🔄 Updates Needed After Integration

### Files to Update

1. **AGENT_ARMY_KNOWLEDGE.md**
   - Add new providers to provider list
   - Update load balancing strategy
   - Document new agent assignments

2. **TODO.md**
   - Mark Task #5 COMPLETE ✅
   - Update with testing results

3. **MEMORY.md**
   - Document integration success
   - Note provider capabilities and limits

---

## ✅ Integration Checklist

### Pre-Integration
- [ ] Sign up for Cloudflare Workers AI dashboard
- [ ] Get Cloudflare Account ID
- [ ] Create Cloudflare API Token
- [ ] Sign up for Mistral La Plateforme
- [ ] Create Mistral API Key

### Configuration
- [ ] Add Cloudflare provider to openclaw.json
- [ ] Add Mistral provider to openclaw.json
- [ ] Verify JSON syntax is valid
- [ ] Backup original openclaw.json

### Testing
- [ ] Test Cloudflare GPT-OSS 120B
- [ ] Test Cloudflare GPT-OSS 20B
- [ ] Test Mistral Tiny
- [ ] Test Mistral Small
- [ ] Test Mistral Medium
- [ ] Test Codestral

### Deployment
- [ ] Restart OpenClaw gateway
- [ ] Verify providers are listed in `/models`
- [ ] Test with actual agent tasks

### Documentation
- [ ] Update AGENT_ARMY_KNOWLEDGE.md
- [ ] Update TODO.md
- [ ] Update MEMORY.md
- [ ] Create integration summary

---

## 📝 Notes

**Cost:**
- Both providers are FREE
- No API costs incurred
- Estimated savings vs. paid alternatives: ~$550/month

**Rate Limits:**
- Cloudflare: 10,000 neurons/day
- Mistral: 1B tokens/month, 1 req/sec
- Monitor usage to stay within limits

**Data Usage:**
- Cloudflare: No training on free tier
- Mistral: Requires opt-in for data training (free tier)

**Reliability:**
- Cloudflare: Enterprise-grade reliability
- Mistral: Production-proven, used by many companies

---

## 🎯 Next Steps After Integration

1. **Add Cerebras** (Task #5b)
   - Qwen 3 235B for large-scale reasoning
   - 1M tokens/day limit

2. **Consider Google AI Studio** (Optional)
   - Multimodal capabilities
   - 250K tokens/minute speed

3. **Monitor Performance**
   - Track provider reliability
   - Optimize load balancing
   - Measure cost savings

---

## 🆘 Troubleshooting

### Common Issues

**Cloudflare 401 Unauthorized:**
- Check API token is correct
- Verify token has "Workers AI Scripts - Edit" permission
- Verify Account ID is correct

**Mistral 401 Unauthorized:**
- Check API key is correct
- Verify key is active in Mistral console

**Model not found:**
- Verify model ID is correct
- Check model is available in free tier

**Rate limit errors:**
- Monitor usage levels
- Implement retry logic
- Fallback to backup provider

---

**Integration Guide Complete**
**Ready for implementation once API keys are obtained**

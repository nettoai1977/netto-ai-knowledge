# Free LLM API Resources Analysis
## Source: https://github.com/cheahjs/free-llm-api-resources

---

## 🔑 PROVEN, HIGH-VALUE FREE PROVIDERS

Already configured in OpenClaw (VERIFY):
**✅ NVIDIA NIM** (https://build.nvidia.com/explore/discover)
- Status: PRIMARY provider (nvidia/z-ai/glm5, nvidia/z-ai/glm4.7, nvidia/llama-3.1-lite)
- Limits: 40 requests/minute (good)
- Current usage: FREE 💚
- Models: 200+ open/proprietary models (GLM, Nemotron, LLaMA)

**✅ Groq** (https://console.groq.com)
- Status: AUTHENTICATED (api.provider: groq in openclaw.json) 💚
- Limits: Up to 14,400 requests/day (Llama 3.1 8B)
- Key free models:
  - Llama 4 Scout Instruct (vision) ✅
  - Llama 4 Maverick 17B 128E (max 1,000/day)
  - Llama 3.3 70B Instruct (max 1,000/day)
  - Llama 3.1 8B (max 14,400/day)
  - Whisper Large v3 (audio)
  - Kimi K2 Instruct (max 1,000/day)
- Recommended: Use Llama 4 Scout for vision, Llama 3.1 8B for rapid small tasks

**✅ OpenRouter** (https://openrouter.ai)
- Status: AUTHENTICATED (auth.profiles.openrouter:default) 💚
- Limits: 20 requests/minute base, 50/day free, up to 1000/day with $10 topup
- Free models (high value):
  - openai/gpt-oss-20b:free
  - openai/gpt-oss-120b:free
  - google/gemma-3-27b-it:free
  - meta-llama/llama-3.3-70b-instruct:free
  - deepseek/deepseek-r1-0528:free (reasoning)
  - stepfun/step-3.5-flash:free
  - z-ai/glm-4.5-air:free
- Recommendation: Use GPT-OSS 120B for deep reasoning, DeepSeek-R1 for analytical tasks

---

## 🚀 NEW HIGH-VALUE PROVIDERS TO INTEGRATE

**1. Cloudflare Workers AI** (https://developers.cloudflare.com/workers-ai)
- Status: NOT CONFIGURED 🆕
- Limits: 10,000 neurons/day FREE
- Key free models:
  - @cf/openai/gpt-oss-120b (strong reasoning)
  - @cf/openai/gpt-oss-20b (fast)
  - @cf/qwen/qwen3-30b-a3b-fp8 (Chinese/English)
  - @cf/zai-org/glm-4.7-flash (GLM fast)
  - DeepSeek R1 Distill Qwen 32B (reasoning)
- Integration value: Backup reasoning agent, reduces load on primary providers
- Recommended action: Add to openclaw.json providers

**2. Google AI Studio** (https://aistudio.google.com)
- Status: NOT CONFIGURED 🆕
- Limits: Up to 250,000 tokens/minute (Gemini 3 Flash), 20 requests/day
- Models: Gemini 3 / 2.5 Flash, Gemma 3 series (4B, 12B, 27B)
- Key strength: Multimodal + generation speed (250,000 tokens/min is HUGE)
- Limitation: Data used for training when outside UK/CH/EEA/EU
- Recommended action: Add for multimodal tasks + high-speed generation

**3. Mistral (La Plateforme)** (https://console.mistral.ai/)
- Status: NOT CONFIGURED 🆕
- Limits: 1 request/second, 500,000 tokens/minute, 1,000,000,000 tokens/month
- Models: Open-source Mistral + proprietary
- Key feature: 1B tokens/month limit is MASSIVE (10x NVIDIA)
- Limitation: Free tier requires opting into data training
- Recommended action: Add for code/dev (Codestral), high-volume tasks

**4. Cerebras** (https://cloud.cerebras.ai/)
- Status: NOT CONFIGURED 🆕
- Key free models:
  - Qwen 3 235B A22B Instruct (max 14,400/day, 1M tokens/day)
  - Llama 3.3 70B (max 14,400/day, 1M tokens/day)
  - OpenAI GPT-OSS 120B (max 14,400/day)
- Key strength: 1M tokens/day (massive context processing)
- Recommended action: Add for large-scale code review, large file analysis

---

## 📊 COMPARISON TABLE

| Provider | Current Status | Monthly Limit | Best For | Action |
|----------|---------------|----------------|----------|--------|
| **NVIDIA NIM** | ✅ Configured | 40 req/min | Primary tasks | MAINTAIN |
| **Groq** | ✅ Configured | Up to 14,400/day | Vision, fast token | MAINTAIN |
| **OpenRouter** | ✅ Configured | 50-1,000 req/day | Deep reasoning | MAINTAIN |
| **Cloudflare Workers** | ❌ NOT config | 10,000 neurons/day | Backup reasoning | **ADD NOW** |
| **Google AI Studio** | ❌ NOT config | 20 req/day | Multimodal, speed | **CONSIDER** |
| **Mistral La Plateforme** | ❌ NOT config | 1B tokens/month | High-volume | **ADD NOW** |
| **Cerebras** | ❌ NOT config | 14,400 req/day | Large-scale | **ADD NOW** |

---

## 🎯 INTEGRATION PRIORITY

### HIGH Priority (Add Now):
1. **Cloudflare Workers AI** - Backup reasoning agent, GPT-OSS 120B
2. **Mistral La Plateforme** - 1B tokens/month (massive), code/dev focus

### MEDIUM Priority (Consider):
3. **Cerebras** - Qwen 3 235B for large-scale reasoning
4. **Google AI Studio** - Multimodal + speed (but data training opt-in)

### LOW Priority (Test Later):
- HuggingFace Inference Providers ($0.10/month - minimal value)
- Vercel AI Gateway ($5/month - not free)
- Cohere (1,000 req/month - too restrictive)

---

## 🔄 LOAD BALANCING UPDATE

With new providers integrated, update load balancing strategy:

**Priority 1: FREE Fast Tasks**
- Flash (existing)
- Groq: Llama 3.1 8B (14,400 requests/day)

**Priority 2: FREE Reasoning Tasks**
- Atlas/Zen: NVIDIA GLM 4.7
- Backup: OpenRouter GPT-OSS 120B
- Fallback: Cloudflare GPT-OSS 120B

**Priority 3: FREE High-Volume Processing**
- Large tasks: Mistral La Plateforme (1B tokens/month)
- Extra backup: Cerebras Qwen 3 235B (1M tokens/day)

**Priority 4: FREE Vision/Multimodal**
- Vision: Groq Llama 4 Scout
- Multimodal: Google AI Studio Gemini 3 Flash

---

## 💰 COST SAVINGS BY INTEGRATION

**Estimated Savings (per integration):**
- Cloudflare Workers: 10,000 neurons/day (equivalent to ~$50/month)
- Mistral La Plateforme: 1B tokens/month (equivalent to ~$200/month at $0.20/1M)
- Cerebras: 1M tokens/day (30M/month) (equivalent to ~$300/month at $0.01/1K)
- **TOTAL POTENTIAL SAVINGS: ~$550/month**

**Current Cost:** $0/month ✅
**With Integrations:** Still $0/month (all free) ✅
**Value:** Increased capacity and redundancy at no cost

---

## 📋 NEXT ACTIONS

### Immediate (Days 1-3):
1. Add Cloudflare Workers AI to openclaw.json providers
2. Add Mistral La Plateforme to openclaw.json providers
3. Test integration with sample tasks

### Medium (Days 4-7):
4. Add Cerebras for large-scale tasks
5. Consider Google AI Studio for multimodal (decide on data training opt-in)
6. Update AGENT_ARMY_KNOWLEDGE.md with new provider info

### Long-term (Week 6+):
7. Monitor provider reliability and performance
8. Optimize load balancing with 4+ providers
9. Add to cost optimization automation

---

## 📚 PROVEN REFERENCES

The free-llm-api-resources repository:
- GitHub: https://github.com/cheahjs/free-llm-api-resources
- Last verified: February 18, 2026
- Provider list verified against documentation
- All providers listed are legitimate (no reverse engineering)
- Warning: Don't abuse to preserve free access

---

## ⚠️ IMPORTANT NOTES

**Provider Verification:**
- All providers in list are legitimate
- No reverse-engineered chatbot APIs included
- Respect rate limits to maintain free access

**Data Training Opt-In:**
- Google AI Studio: Data used for training outside UK/CH/EEA/EU
- Mistral La Plateforme: Requires opt-in for free tier
- Others: Typically no training for free tiers

**Rate Limits:**
- Monitor actual usage vs limits
- Implement retry logic for rate limited requests
- Prioritize stable providers (NVIDIA, Groq) for core operations

---

**Analysis Complete: February 18, 2026**

---

*Next Step: Decide on provider integration (start with Cloudflare + Mistral)*

---

## 🎯 RECOMMENDATION: START WITH 2 PROVIDERS

**Option 1: Add Both High-Priority Providers**
- Cloudflare Workers AI + Mistral La Plateforme
- Backup reasoning + high-volume processing
- Zero cost, massive capacity increase

**Option 2: Add Only Cloudflare Workers**
- Backup reasoning first
- Test and validate before adding Mistral
- Slower pace, more testing

**Option 3: Skip Integration**
- Continue with existing NVIDIA + Groq + OpenRouter
- Focus on current deployment (cron, load balancing)
- No new providers now

---

**What would you like to do?** 🎯

1. Start integration with Cloudflare + Mistral La Plateforme
2. Start integration with Cloudflare only
3. Skip integration, continue with Week 5 deployment
4. Something else (specify)

# Rate Limit Bypass Strategy

## Problem
NVIDIA API free tier has limits:
- **40 requests per minute (RPM)**
- Concurrent requests trigger 429 errors
- Subagent spawning (4-8 parallel) exhausts quota instantly

## Provider Rate Limits (Free Tiers)

| Provider | RPM Limit | TPM Limit | Notes |
|----------|-----------|-----------|-------|
| NVIDIA | 40 | Unlimited | Free, 200K context |
| Groq | 30 | 12,000 TPM | Free, fast inference |
| Cloudflare | 300+ | Unlimited | Free, 128K context |
| OpenRouter | 20 | Variable | Free tier limited |
| xAI | 60 | Unknown | Grok 4 |

## Solution: Multi-Provider Load Balancing

### 1. Provider Priority Chain
When rate-limited, auto-fallback:
```
NVIDIA (primary) → Cloudflare → Groq → OpenRouter → xAI
```

### 2. Subagent Model Distribution
Assign different providers to different agents to avoid collision:

| Agent | Model | Provider |
|-------|-------|----------|
| main | GLM 5 | NVIDIA |
| atlas | GPT-OSS 120B | Cloudflare |
| luna | GLM 4.7 | NVIDIA |
| orion | DeepSeek R1 | Cloudflare |
| nova | Kimi K2.5 | NVIDIA |
| zen | GPT-OSS 120B | Cloudflare |
| flash | GLM 5 | NVIDIA |
| titan | Llama 3.3 70B | Groq |
| coder | Devstral 2 | NVIDIA |
| max | Mistral Large 3 | NVIDIA |
| spark | Ministral 14B | NVIDIA |
| vision | Llama 4 Scout | Groq |

### 3. Sequential Subagent Spawning
Instead of spawning 4-8 agents in parallel:
- Spawn one at a time
- Wait for completion before next
- Or stagger with 2-second delays

### 4. Request Queueing
Implement retry logic:
- On 429: Wait 2 seconds, retry with different provider
- Track requests per minute
- Cache frequently used data

## Implementation Status
- [ ] Configure provider fallback chain
- [ ] Assign models to agents
- [ ] Implement sequential spawning
- [ ] Add retry logic

## Benefits
- **No downtime** - Always have a working provider
- **No cost** - All free tiers
- **High availability** - Distributed across 5 providers
- **Better throughput** - 150+ RPM combined capacity

# Multi-Timeframe Market Matrix

## 📊 System Overview

The Multi-Timeframe Market Matrix is a **paper trading analysis system** that monitors cryptocurrency markets across four timeframes using live CCXT data. It implements an **anti-hallucination protocol** (Radar Agent) to ensure all data is real and verified.

### Core Principles

1. **Rule 1: Anti-Hallucination** — Never guess or fabricate price, RSI, or trend data. All data must be pulled via CCXT and verified by Radar before reporting.

2. **Rule 2: Paper Trading Only** — The system identifies opportunities; the human is the trigger. No automatic execution.

---

## ⏰ Timeframe Schedule

| Timeframe | Schedule | Cron Expression | Purpose |
|-----------|----------|-----------------|---------|
| **Daily Macro** | 7:00 AM NZT | `0 7 * * *` | Establish macro bias for the day |
| **4H Outlook** | Every 4 hours | `0 */4 * * *` | Monitor trend alignment with daily |
| **1H Shift** | Every hour | `0 * * * *` | Detect early warning signs |
| **15m Tactical** | Every 15 min | `*/15 * * * *` | Find actionable setups |

---

## 📅 Daily Macro Report (7:00 AM NZT)

### Purpose
Establishes the **Macro Bias** for the day. This is the foundation for all intraday analysis.

### Data Points Generated

| Metric | Description | Source |
|--------|-------------|--------|
| **Price Action** | Current price, 24h change, high/low | CCXT OHLCV |
| **Trend** | Bullish/Bearish/Ranging (EMA alignment) | Calculated |
| **RSI** | 14-period RSI, condition (OB/OS) | Calculated |
| **ATR** | Average True Range, volatility % | Calculated |
| **EMA Stack** | EMA9, EMA21, EMA50 alignment | Calculated |
| **Support/Resistance** | Key levels from pivot points | Calculated |
| **Volume** | Current vs 20-period average | CCXT OHLCV |
| **Macro Bias** | BULLISH/BEARISH/NEUTRAL/CAUTION | Synthesized |

### Macro Bias Logic

```
IF Daily trend = BULLISH AND RSI < 70 AND strength > 60%
   → BULLISH_BIAS
   
IF Daily trend = BEARISH AND RSI > 30 AND strength > 60%
   → BEARISH_BIAS
   
IF RSI > 70
   → CAUTION_LONGS
   
IF RSI < 30
   → CAUTION_SHORTS
   
ELSE
   → NEUTRAL
```

### Watchlist

```javascript
[
  'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT',
  'XRP/USDT', 'DOGE/USDT', 'ADA/USDT', 'AVAX/USDT',
  'LINK/USDT', 'DOT/USDT'
]
```

---

## ⏰ 4-Hour Outlook Monitor

### Purpose
Compare 4H trend to Daily Macro Bias. Alert only on significant changes.

### Alert Conditions

| Condition | Alert |
|-----------|-------|
| **Alignment** | 4H trend = Daily trend → Potential macro setup |
| **Divergence** | MACD histogram opposite to trend → Warning |
| **Resistance Test** | Price within 1% of resistance → Level watch |
| **Support Test** | Price within 1% of support → Level watch |

### Output
- **Only alerts** when conditions met
- Silent otherwise (internal logging only)

---

## 🕐 1-Hour Shift Monitor

### Purpose
Detect intraday shifts that contradict the 4H outlook.

### Alert Conditions

| Condition | Threshold | Alert |
|-----------|-----------|-------|
| **Volume Spike** | Volume > 2x average | 📊 Volume alert |
| **Support Break** | Price < support * 0.99 | 🔴 Support break |
| **Resistance Break** | Price > resistance * 1.01 | 🟢 Resistance break |
| **Exhaustion** | RSI > 75 (bull) or < 25 (bear) | ⚠️ Trend exhaustion |

### Output
- Alerts sent when conditions triggered
- Silent when no shifts detected

---

## ⚡ 15-Minute Tactical Scanner

### Purpose
Find immediate, actionable paper-trading setups with confluence verification.

### Confluence Scoring (1-10)

| Factor | Weight | Points |
|--------|--------|--------|
| Daily trend direction | 3 | 3 if bullish/bearish |
| 4H alignment with Daily | 2 | 2 if aligned |
| 1H alignment with Daily | 2 | 2 if aligned |
| 15m RSI setup | 2 | 2 if OB/OS matches trend |
| Price near key level | 1 | +1 if near S/R |

### Minimum Threshold
**Confluence Score ≥ 6** required for signal generation

### Signal Output Format

```
🚨 ACTIONABLE SIGNAL DETECTED
────────────────────────────────
💱 ADA/USDT
📈 Side: SHORT
🎯 Confluence Score: 6/10
📊 Factors: Daily bearish, 1H aligned, Near support
📍 Entry: $0.28120000
🛡️ Stop Loss: $0.28257143 (0.49%)
🎯 Take Profit: $0.27845714 (0.97%)
📊 R:R Ratio: 2.0
────────────────────────────────
⚠️ PAPER TRADING ONLY - Human confirmation required
```

### Trade Level Calculation

```
ATR = 14-period Average True Range

LONG:
  Entry = Current Price
  Stop Loss = Entry - (ATR × 1.5)
  Take Profit = Entry + (ATR × 3)
  
SHORT:
  Entry = Current Price
  Stop Loss = Entry + (ATR × 1.5)
  Take Profit = Entry - (ATR × 3)
```

Risk:Reward = **2:1** by default

---

## 📡 Radar Agent (Anti-Hallucination Protocol)

### Purpose
Verify ALL data before use. Reject anything that doesn't pass validation.

### Verification Checks

| Check | Description | Rejection Reason |
|-------|-------------|------------------|
| **Data Existence** | OHLCV array not empty | "Empty data" |
| **Freshness** | Last candle < 2x timeframe old | "Stale data" |
| **Candle Structure** | Each candle has 6 values | "Invalid structure" |
| **Price Validity** | All prices > 0 | "Invalid prices" |
| **OHLC Consistency** | High ≥ Low, High ≥ Open/Close, Low ≤ Open/Close | "Price consistency error" |
| **RSI Bounds** | 0 ≤ RSI ≤ 100 | "RSI out of bounds" |

### Rejection Log
All rejected data is logged with timestamp, symbol, timeframe, and reason.

---

## 🔧 Technical Implementation

### CCXT Integration

```javascript
const ccxt = require('ccxt');
const exchange = new ccxt.binance({ enableRateLimit: true });

// Fetch OHLCV
const ohlcv = await exchange.fetchOHLCV('BTC/USDT', '1d', undefined, 100);

// Returns: [timestamp, open, high, low, close, volume]
```

### Data Flow

```
CCXT API
    ↓
Radar Verification
    ↓ (REJECTED → Log & Skip)
    ↓ (VERIFIED → Continue)
Technical Indicators
    ↓
Confluence Calculation
    ↓
Signal Generation
    ↓
Dashboard Update
```

### File Outputs

| File | Location | Content |
|------|----------|---------|
| Daily Reports | `matrix-data/daily-macro-*.json` | Full daily analysis |
| 4H Reports | `matrix-data/4h-outlook-*.json` | Alignment checks |
| 1H Reports | `matrix-data/1h-shift-*.json` | Shift alerts |
| 15m Reports | `matrix-data/15m-tactical-*.json` | Signal alerts |

---

## 🎛️ Configuration

### Indicator Settings

```javascript
{
  emaFast: 9,
  emaSlow: 21,
  emaMacro: 50,
  rsiPeriod: 14,
  atrPeriod: 14,
  bollingerPeriod: 20,
  bollingerStdDev: 2
}
```

### Paper Trading Settings

```javascript
{
  riskPerTrade: 0.02,    // 2% risk per trade
  rewardRiskRatio: 2,    // 2:1 R:R
  maxPositions: 5        // Max concurrent positions
}
```

---

## 📱 Cron Job Configuration

### Current Jobs

| Job ID | Name | Schedule | Next Run |
|--------|------|----------|----------|
| `416a1140...` | Daily Macro Report | 7:00 AM NZT | Mon Feb 23 @ 07:00 |
| `2be88549...` | 4-Hour Outlook Monitor | Every 4h | Today @ 12:00 PM |
| `5e8b6d81...` | 1-Hour Shift Monitor | Hourly | Today @ 11:00 AM |
| `d72ebd19...` | 15-Min Tactical Scanner | Every 15m | Today @ 11:00 AM |

### Manual Execution

```bash
# Run individual reports
node market-matrix.js daily    # Daily Macro
node market-matrix.js 4h       # 4-Hour Outlook
node market-matrix.js 1h       # 1-Hour Shift
node market-matrix.js 15m      # 15-Min Tactical

# Run all reports
node market-matrix.js scan

# Analyze specific symbol
node market-matrix.js analyze BTC/USDT

# Test connection
node market-matrix.js test
```

---

## 📊 Dashboard Access

### Location
`~/.openclaw/workspace/trading/dashboard.html`

### Open in Browser
```bash
open ~/.openclaw/workspace/trading/dashboard.html
```

### Features
- Real-time stats (capital, P&L, win rate)
- Timeframe status cards
- Live watchlist with trends
- Active signals panel
- Trade history log
- Auto-refresh (30 seconds)

---

## ⚠️ Important Disclaimers

1. **PAPER TRADING ONLY** — This system does not execute real trades
2. **Human Trigger Required** — You decide whether to act on signals
3. **Data Verification** — Radar Agent catches hallucinations
4. **No Guarantees** — Past performance ≠ future results
5. **Risk Management** — Always use stop losses, never risk more than you can lose

---

## 🚀 Quick Start

```bash
# 1. Navigate to trading directory
cd ~/.openclaw/workspace/trading

# 2. Test CCXT connection
node market-matrix.js test

# 3. Run a quick scan
node market-matrix.js scan

# 4. Open dashboard
open dashboard.html
```

---

## 📝 File Structure

```
trading/
├── market-matrix.js      # Main scanner script
├── dashboard.html        # Web dashboard
├── matrix-data/          # Report outputs
│   ├── daily-macro-*.json
│   ├── 4h-outlook-*.json
│   ├── 1h-shift-*.json
│   └── 15m-tactical-*.json
├── binance_futures.py    # Binance executor
├── trinity_futures.py    # Trinity orchestrator
├── radar_agent.py        # Radar verification
├── scanner.py            # Market scanner
├── ensemble_engine.py    # Multi-model consensus
└── .env                  # API keys (protected)
```

---

*Created: 2026-02-22 | System: Multi-Timeframe Market Matrix v2.0*
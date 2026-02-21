# TRINITY TRADING SYSTEM

Multi-agent cryptocurrency trading system based on research from three creators:
- **Michael Automates** - OpenClaw + Hyperliquid workflow
- **Aaron Dishner** - TBO indicator, cycle degradation, new listings
- **Across the Rubicon** - 7-agent architecture, circuit breakers, Radar agent

---

## Architecture

```
┌─────────────────────────────────────────┐
│           TRINITY SYSTEM                 │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ SCANNER │  │ RADAR   │  │EXECUTOR │ │
│  │         │  │         │  │         │ │
│  │ Market  │→ │ Data    │→ │ Paper   │ │
│  │ Analysis│  │ Verify  │  │ Trade   │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      DASHBOARD                  │   │
│  │  Trade Log | P&L | Auditor      │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Components

### 1. Radar Agent (`radar_agent.py`)
**Anti-Hallucination Data Verifier**

- Fetches raw OHLCV from CCXT (no hallucinated data)
- Calculates RSI, MACD, ADX, Bollinger, TBO locally
- Verifies claimed values against calculated values
- Reports VERIFIED or REJECTED status

### 2. Market Scanner (`scanner.py`)
**Multi-Agent Market Scanner**

- Scans top 20 trading pairs
- Calculates confluence score (0-100)
- Filters by regime (ADX + Bollinger)
- Generates LONG/SHORT signals

### 3. Executor (`executor.py`) - Coming Soon
**Paper Trading Executor**

- Circuit breaker (3 losses → STOP)
- Position sizing (Kelly criterion)
- Human trigger required
- Trade logging

---

## Configuration

Set environment variables:

```bash
# Binance Demo/Testnet
export BINANCE_API_KEY="your_demo_api_key"
export BINANCE_API_SECRET="your_demo_secret"
export BINANCE_DEMO=true

# Or Hyperliquid
export HYPERLIQUID_WALLET="your_wallet_address"
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

---

## Risk Management

| Feature | Setting |
|---------|---------|
| Circuit Breaker | 3 losses → STOP |
| Max Position | 5% of capital |
| Max Drawdown | 50% |
| Regime Filter | ADX > 25 required |
| Confluence | 70% minimum |

---

## Usage

```bash
# Install dependencies
pip install ccxt pandas numpy

# Run Radar test
python radar_agent.py

# Run market scan
python scanner.py
```

---

## Key Insights from Research

### Michael Automates
- Backtest BEFORE deployment
- Long-bias reduces drawdown
- AI reflects and adapts
- ~$500/month on Claude

### Aaron Dishner
- 97% of coins degrade cycle-over-cycle
- New listings = 10x-100x potential
- TBO: 20 EMA cross 40 EMA
- Focus on first-cycle coins

### Across the Rubicon
- 7-agent squad architecture
- Radar for safety auditing
- Circuit breakers save capital
- Monte Carlo validation

---

## Status

- [x] Radar agent (data verification)
- [x] Market scanner (signal generation)
- [x] Ensemble engine (multi-model consensus)
- [x] Trinity orchestrator (main entry point)
- [ ] Paper trade executor
- [ ] Dashboard
- [ ] Cron job scheduler

---

## Disclaimer

**This is for educational and paper trading purposes only.**

- Never trade with real money until thoroughly tested
- Always use testnet/demo mode first
- Past performance does not guarantee future results
- Cryptocurrency trading involves significant risk of loss

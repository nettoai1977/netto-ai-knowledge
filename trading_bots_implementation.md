# Crypto Trading Bots Implementation Guide

## 🎯 1. CRYPTO SIGNALS TRADING BOT

### Overview
Automated bot that executes trades based on technical indicator signals (RSI, MACD, SMA/EMA crossovers).

### Implementation Steps

#### Step 1: Signal Detection Logic
```javascript
// signal-bot.js
const detectSignals = (symbol, timeframe) => {
  const rsi = calculateRSI(symbol, timeframe);
  const macd = calculateMACD(symbol, timeframe);
  const emaShort = calculateEMA(symbol, 9, timeframe);
  const emaLong = calculateEMA(symbol, 21, timeframe);
  
  let signal = null;
  
  // BUY Signal
  if (rsi < 30 && macd.histogram > 0 && emaShort > emaLong) {
    signal = { side: 'BUY', strength: calculateConfluence(rsi, macd, ema) };
  }
  // SELL Signal
  else if (rsi > 70 && macd.histogram < 0 && emaShort < emaLong) {
    signal = { side: 'SELL', strength: calculateConfluence(rsi, macd, ema) };
  }
  
  return signal;
};
```

#### Step 2: Risk Management
```javascript
const executeTrade = (signal, symbol) => {
  if (signal.strength < 6) return; // Min confluence threshold
  
  const balance = getBalance();
  const risk = balance * 0.02; // 2% risk per trade
  const entry = getCurrentPrice(symbol);
  const stopLoss = signal.side === 'BUY' 
    ? entry * 0.985 // 1.5% stop
    : entry * 1.015;
  const takeProfit = signal.side === 'BUY'
    ? entry * 1.03 // 3% target
    : entry * 0.97;
  
  const quantity = risk / Math.abs(entry - stopLoss);
  
  placeOrder({
    symbol,
    side: signal.side,
    quantity,
    stopLoss,
    takeProfit
  });
};
```

#### Step 3: Cron Schedule
```bash
# Check signals every 15 minutes
*/15 * * * * cd ~/.openclaw/workspace/trading && node signal-bot.js
```

### Configuration File
```json
{
  "signal_bot": {
    "enabled": true,
    "timeframe": "15m",
    "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
    "min_confluence": 6,
    "risk_per_trade": 0.02,
    "max_positions": 5,
    "indicators": {
      "rsi_period": 14,
      "rsi_overbought": 70,
      "rsi_oversold": 30,
      "macd_fast": 12,
      "macd_slow": 26,
      "macd_signal": 9
    }
  }
}
```

### Pros & Cons
✅ **Pros:**
- Fast reaction to market changes
- Can catch trend reversals early
- Flexible indicator combinations

❌ **Cons:**
- False signals in ranging markets
- Requires fine-tuning
- Can be whipsawed

---

## 💰 2. CRYPTO DCA (DOLLAR-COST AVERAGING) BOT

### Overview
Automated recurring purchases of fixed amounts regardless of price. Reduces volatility impact.

### Implementation Steps

#### Step 1: Basic DCA Logic
```javascript
// dca-bot.js
const executeDCA = async () => {
  const config = {
    BTC: { amount: 100, symbol: 'BTCUSDT' },
    ETH: { amount: 100, symbol: 'ETHUSDT' },
    BNB: { amount: 50, symbol: 'BNBUSDT' }
  };
  
  for (const [asset, settings] of Object.entries(config)) {
    const price = await getPrice(settings.symbol);
    const quantity = settings.amount / price;
    
    await placeOrder({
      symbol: settings.symbol,
      side: 'BUY',
      quantity: quantity,
      type: 'MARKET'
    });
    
    logPurchase(asset, settings.amount, price, quantity);
  }
};
```

#### Step 2: Advanced DCA (Price-Based)
```javascript
// Buy on dips
const executeDipDCA = async () => {
  const dips = {
    BTC: { threshold: -0.05, amount: 150 }, // Buy if BTC drops 5%
    ETH: { threshold: -0.07, amount: 100 } // Buy if ETH drops 7%
  };
  
  for (const [asset, config] of Object.entries(dips)) {
    const priceChange = get24hChange(asset);
    if (priceChange <= config.threshold) {
      await buyAsset(asset, config.amount);
    }
  }
};
```

#### Step 3: Cron Schedule
```bash
# Weekly DCA (Mondays at 9 AM)
0 9 * * 1 cd ~/.openclaw/workspace/trading && node dca-bot.js

# Daily DCA (9 AM every day)
0 9 * * * cd ~/.openclaw/workspace/trading && node dca-bot.js

# Dip DCA (check hourly)
0 * * * * cd ~/.openclaw/workspace/trading && node dip-dca-bot.js
```

### Configuration File
```json
{
  "dca_bot": {
    "enabled": true,
    "schedule": "weekly", // daily, weekly, monthly
    "day": "monday",
    "time": "09:00",
    "assets": {
      "BTCUSDT": { "amount": 100, "currency": "USDT" },
      "ETHUSDT": { "amount": 100, "currency": "USDT" },
      "BNBUSDT": { "amount": 50, "currency": "USDT" }
    },
    "dip_mode": {
      "enabled": true,
      "check_interval": "1h",
      "thresholds": {
        "BTC": -0.05,
        "ETH": -0.07,
        "BNB": -0.10
      }
    }
  }
}
```

### Pros & Cons
✅ **Pros:**
- Removes emotion from investing
- Smooths out volatility
- Great for long-term accumulation
- Easy to automate

❌ **Cons:**
- Binds capital regularly
- May buy at unfavorable prices during trends
- Slower to build positions

---

## 📊 3. CRYPTO GRID TRADING BOT

### Overview
Places buy/sell orders at regular price intervals. Profits from sideways price movement.

### Implementation Steps

#### Step 1: Grid Setup
```javascript
// grid-bot.js
const createGrid = (symbol, lowerPrice, upperPrice, gridCount) => {
  const gridSize = (upperPrice - lowerPrice) / gridCount;
  const grids = [];
  
  for (let i = 0; i <= gridCount; i++) {
    const price = lowerPrice + (gridSize * i);
    grids.push({
      buyPrice: price - gridSize,
      sellPrice: price,
      level: i
    });
  }
  
  return grids;
};
```

#### Step 2: Order Placement
```javascript
const deployGrid = async (symbol, grids, totalInvestment) => {
  const pricePerGrid = totalInvestment / grids.length;
  const orders = [];
  
  for (const grid of grids) {
    if (grid.buyPrice > 0) {
      // Place buy order
      const buyOrder = await placeLimitOrder({
        symbol,
        side: 'BUY',
        price: grid.buyPrice,
        quantity: pricePerGrid / grid.buyPrice
      });
      orders.push({ grid, buyOrder, status: 'pending' });
    }
  }
  
  return orders;
};
```

#### Step 3: Grid Management
```javascript
const monitorGrid = async (orders) => {
  for (const order of orders) {
    const status = await checkOrderStatus(order.buyOrder.id);
    
    if (status === 'FILLED') {
      // Place corresponding sell order
      await placeLimitOrder({
        symbol: order.buyOrder.symbol,
        side: 'SELL',
        price: order.grid.sellPrice,
        quantity: order.buyOrder.quantity
      });
      
      // Place new buy order one level down
      const newLevel = order.grid.level - 1;
      if (newLevel >= 0) {
        await placeGridBuyOrder(order.grid.symbol, newLevel);
      }
    }
  }
};
```

#### Step 4: Cron Schedule
```bash
# Grid monitoring (every 5 minutes)
*/5 * * * * cd ~/.openclaw/workspace/trading && node grid-bot.js

# Grid rebalancing (daily)
0 0 * * * cd ~/.openclaw/workspace/trading && node grid-rebalance.js
```

### Configuration File
```json
{
  "grid_bot": {
    "enabled": true,
    "symbol": "BTCUSDT",
    "settings": {
      "lower_price": 60000,
      "upper_price": 70000,
      "grid_count": 10,
      "investment": 1000,
      "grid_spacing": "arithmetic" // or "geometric"
    },
    "risk_management": {
      "stop_loss": 0.10, // Stop bot if price drops 10% below lower bound
      "take_profit": 0.15, // Take profit if price rises 15% above upper bound
      "rebalance": true
    },
    "monitoring": {
      "interval": "5m",
      "rebate_interval": "1d"
    }
  }
}
```

### Pros & Cons
✅ **Pros:**
- Profits from sideways markets
- No prediction needed
- Scales well
- Automated execution

❌ **Cons:**
- Loses in strong trends
- Requires proper range selection
- Capital locked
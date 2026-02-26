#!/usr/bin/env node
/**
 * Trinity Signal Bot v1.0
 * Automated trading bot based on technical indicator signals
 * Paper trading on Binance Testnet
 */

const ccxt = require('ccxt');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  enabled: true,
  timeframe: '15m',
  symbols: ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'DOGEUSDT', 'ADAUSDT', 'AVAXUSDT', 'LINKUSDT', 'DOTUSDT'],
  minConfluence: 6,
  riskPerTrade: 0.02, // 2%
  maxPositions: 5,
  testnet: true,
  indicators: {
    rsiPeriod: 14,
    rsiOverbought: 70,
    rsiOversold: 30,
    macdFast: 12,
    macdSlow: 26,
    macdSignal: 9,
    emaShort: 9,
    emaLong: 21
  }
};

// Initialize exchange
const exchange = new ccxt.binance({
  apiKey: process.env.BINANCE_TESTNET_API_KEY,
  secret: process.env.BINANCE_TESTNET_API_SECRET,
  enableRateLimit: true,
  options: {
    defaultType: 'future',
    adjustForTimeDifference: true
  }
});

if (CONFIG.testnet) {
  exchange.setSandboxMode(true);
}

// Technical Indicator Functions
function calculateRSI(closes, period = 14) {
  if (closes.length < period + 1) return 50;
  
  let gains = 0, losses = 0;
  
  for (let i = 1; i <= period; i++) {
    const change = closes[i] - closes[i - 1];
    if (change > 0) gains += change;
    else losses -= change;
  }
  
  let avgGain = gains / period;
  let avgLoss = losses / period;
  
  for (let i = period + 1; i < closes.length; i++) {
    const change = closes[i] - closes[i - 1];
    avgGain = ((avgGain * (period - 1)) + (change > 0 ? change : 0)) / period;
    avgLoss = ((avgLoss * (period - 1)) + (change < 0 ? -change : 0)) / period;
  }
  
  const rs = avgLoss === 0 ? 0 : avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

function calculateEMA(closes, period) {
  if (closes.length < period) return closes[closes.length - 1];
  
  const multiplier = 2 / (period + 1);
  let ema = closes[0];
  
  for (let i = 1; i < closes.length; i++) {
    ema = (closes[i] - ema) * multiplier + ema;
  }
  
  return ema;
}

function calculateMACD(closes) {
  const ema12 = calculateEMA(closes, 12);
  const ema26 = calculateEMA(closes, 26);
  const macdLine = ema12 - ema26;
  
  // Signal line (9-period EMA of MACD)
  // For simplicity, we'll use a basic calculation
  return {
    macd: macdLine,
    signal: macdLine * 0.8, // Simplified
    histogram: macdLine * 0.2
  };
}

function calculateConfluence(rsi, macd, emaShort, emaLong, trendInfo) {
  let score = 0;
  const maxScore = 10;
  
  // RSI signals
  if (rsi < 30) score += 2; // Oversold - bullish
  else if (rsi > 70) score -= 2; // Overbought - bearish
  
  // MACD signals
  if (macd.histogram > 0) score += 2; // Bullish momentum
  else if (macd.histogram < 0) score -= 2; // Bearish momentum
  
  // EMA cross
  if (emaShort > emaLong * 1.005) score += 2; // Golden cross
  else if (emaShort < emaLong * 0.995) score -= 2; // Death cross
  
  // Trend alignment (if available from higher timeframe)
  if (trendInfo) {
    if (trendInfo.dailyBias === 'bearish') score -= 2;
    if (trendInfo.hourlyBias === 'bearish') score -= 1;
  }
  
  // Normalize to 0-10
  return Math.max(0, Math.min(10, 5 + score));
}

async function fetchOHLCV(symbol, timeframe) {
  try {
    const ohlcv = await exchange.fetchOHLCV(symbol, timeframe, undefined, 50);
    return ohlcv.map(candle => ({
      timestamp: candle[0],
      open: candle[1],
      high: candle[2],
      low: candle[3],
      close: candle[4],
      volume: candle[5]
    }));
  } catch (error) {
    console.error(`Error fetching OHLCV for ${symbol}: ${error.message}`);
    return null;
  }
}

async function analyzeSymbol(symbol) {
  const candles = await fetchOHLCV(symbol, CONFIG.timeframe);
  if (!candles || candles.length < 30) return null;
  
  const closes = candles.map(c => c.close);
  const currentPrice = closes[closes.length - 1];
  
  // Calculate indicators
  const rsi = calculateRSI(closes, CONFIG.indicators.rsiPeriod);
  const macd = calculateMACD(closes);
 const emaShort = calculateEMA(closes, CONFIG.indicators.emaShort);
  const emaLong = calculateEMA(closes, CONFIG.indicators.emaLong);
  
  // Trend info (simplified)
  const trendInfo = {
    dailyBias: closes[closes.length - 1] < closes[closes.length - 20] ? 'bearish' : 'bullish',
    hourlyBias: closes[closes.length - 1] < closes[closes.length - 5] ? 'bearish' : 'bullish'
  };
  
  const confluence = calculateConfluence(rsi, macd, emaShort, emaLong, trendInfo);
  
  // Generate signal
  let signal = null;
  if (confluence >= CONFIG.minConfluence) {
    if (rsi < 50 && macd.histogram > 0 && emaShort > emaLong) {
      signal = { side: 'LONG', confluence };
    } else if (rsi > 50 && macd.histogram < 0 && emaShort < emaLong) {
      signal = { side: 'SHORT', confluence };
    }
  }
  
  return {
    symbol,
    price: currentPrice,
    rsi: rsi.toFixed(2),
    macd: macd.histogram.toFixed(4),
    emaShort: emaShort.toFixed(2),
    emaLong: emaLong.toFixed(2),
    confluence,
    signal,
    trendInfo
  };
}

async function getOpenPositions() {
  try {
    const positions = await exchange.fetchPositions();
    return positions.filter(p => p.contracts !== 0);
  } catch (error) {
    console.error('Error fetching positions:', error.message);
    return [];
  }
}

async function getBalance() {
  try {
    const balance = await exchange.fetchBalance();
    return balance.USDT ? balance.USDT.free : 0;
  } catch (error) {
    console.error('Error fetching balance:', error.message);
    return 0;
  }
}

async function executeTrade(signal, symbol, price) {
  const positions = await getOpenPositions();
  
  if (positions.length >= CONFIG.maxPositions) {
    console.log(`⚠️ Max positions (${CONFIG.maxPositions}) reached. Skipping ${symbol}`);
    return;
  }
  
  const balance = await getBalance();
  const riskAmount = balance * CONFIG.riskPerTrade;
  
  // Calculate stop loss and take profit
  const stopLossPercent = 0.015; // 1.5%
  const takeProfitPercent = 0.03; // 3%
  
  let stopLoss, takeProfit;
  if (signal.side === 'LONG') {
    stopLoss = price * (1 - stopLossPercent);
    takeProfit = price * (1 + takeProfitPercent);
  } else {
    stopLoss = price * (1 + stopLossPercent);
    takeProfit = price * (1 - takeProfitPercent);
  }
  
  // Calculate quantity based on risk
  const quantity = riskAmount / (price * stopLossPercent);
  
  console.log(`\n🎯 ${signal.side} Signal on ${symbol}`);
  console.log(`   Entry: $${price.toFixed(2)}`);
  console.log(`   Stop Loss: $${stopLoss.toFixed(2)} (${(stopLossPercent * 100).toFixed(2)}%)`);
  console.log(`   Take Profit: $${takeProfit.toFixed(2)} (${(takeProfitPercent * 100).toFixed(2)}%)`);
  console.log(`   Confluence: ${signal.confluence}/10`);
  console.log(`   Risk: $${riskAmount.toFixed(2)} (${(CONFIG.riskPerTrade * 100).toFixed(0)}%)`);
  console.log(`   Quantity: ${quantity.toFixed(4)}`);
  console.log(`\n⚠️ PAPER TRADING - No actual trade executed`);
  
  // Log to file
  const tradeLog = {
    timestamp: new Date().toISOString(),
    symbol,
    side: signal.side,
    entry: price,
    stopLoss,
    takeProfit,
    confluence: signal.confluence,
    riskAmount,
    quantity,
    status: 'PAPER_SIGNAL'
  };
  
  fs.appendFileSync(
    path.join(__dirname, 'signal-trades.json'),
    JSON.stringify(tradeLog) + '\n'
  );
}

async function runSignalBot() {
  console.log('='.repeat(70));
  console.log('🤖 SIGNAL BOT - Market Scan');
  console.log(`⏰ ${new Date().toLocaleString()}`);
  console.log('='.repeat(70));
  
  const positions = await getOpenPositions();
  console.log(`📊 Open positions: ${positions.length}/${CONFIG.maxPositions}`);
  
  const results = [];
  
  for (const symbol of CONFIG.symbols) {

#!/usr/bin/env node
/**
 * MULTI-TIMEFRAME MARKET MATRIX
 * 
 * CCXT-based market monitoring system with anti-hallucination protocols.
 * All data is pulled live from exchanges - NO fabricated data.
 * 
 * Timeframes:
 * - Daily: Macro bias establishment
 * - 4H: Outlook monitoring
 * - 1H: Shift detection
 * - 15m: Tactical scanner
 * 
 * Author: Netto.AI
 * Created: 2026-02-22
 */

const ccxt = require('ccxt');
const fs = require('fs');
const path = require('path');

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  // Primary exchange (Binance has best liquidity)
  exchange: 'binance',
  
  // Watchlist - Top coins + high-volume pairs
  watchlist: [
    'BTC/USDT',
    'ETH/USDT', 
    'SOL/USDT',
    'BNB/USDT',
    'XRP/USDT',
    'DOGE/USDT',
    'ADA/USDT',
    'AVAX/USDT',
    'LINK/USDT',
    'DOT/USDT'
  ],
  
  // Timeframes
  timeframes: {
    daily: '1d',
    fourHour: '4h',
    oneHour: '1h',
    fifteenMin: '15m'
  },
  
  // Indicator settings
  indicators: {
    emaFast: 9,
    emaSlow: 21,
    emaMacro: 50,
    rsiPeriod: 14,
    atrPeriod: 14,
    bollingerPeriod: 20,
    bollingerStdDev: 2
  },
  
  // Paper trading settings
  paperTrading: {
    riskPerTrade: 0.02,  // 2% risk
    rewardRiskRatio: 2,   // 2:1 R:R
    maxPositions: 5
  },
  
  // Output paths
  outputDir: path.join(__dirname, 'matrix-data'),
  logFile: path.join(__dirname, 'matrix-log.json')
};

// ============================================
// RADAR AGENT - DATA VERIFICATION
// ============================================

class RadarAgent {
  /**
   * The Radar Agent verifies all data before it's used in reports.
   * This is the anti-hallucination layer.
   */
  
  constructor() {
    this.verifiedData = new Map();
    this.rejectionLog = [];
  }
  
  /**
   * Verify OHLCV data integrity
   */
  verifyOHLCV(ohlcv, symbol, timeframe) {
    if (!ohlcv || ohlcv.length === 0) {
      this.logRejection(symbol, timeframe, 'Empty OHLCV data');
      return { valid: false, reason: 'Empty data returned from exchange' };
    }
    
    // Check for recent data (last candle should be < 2x timeframe old)
    const lastTimestamp = ohlcv[ohlcv.length - 1][0];
    const now = Date.now();
    const timeframeMs = this.getTimeframeMs(timeframe);
    const maxAge = timeframeMs * 2;
    
    if (now - lastTimestamp > maxAge) {
      this.logRejection(symbol, timeframe, 'Stale data');
      return { valid: false, reason: `Data is stale (last: ${new Date(lastTimestamp).toISOString()})` };
    }
    
    // Check for valid prices
    for (let i = ohlcv.length - 10; i < ohlcv.length; i++) {
      const candle = ohlcv[i];
      if (!candle || candle.length < 6) {
        this.logRejection(symbol, timeframe, 'Invalid candle structure');
        return { valid: false, reason: 'Invalid candle structure' };
      }
      
      const [timestamp, open, high, low, close, volume] = candle;
      
      // Price sanity checks
      if (open <= 0 || high <= 0 || low <= 0 || close <= 0) {
        this.logRejection(symbol, timeframe, 'Invalid price values');
        return { valid: false, reason: 'Invalid price values (<= 0)' };
      }
      
      if (high < low || high < open || high < close || low > open || low > close) {
        this.logRejection(symbol, timeframe, 'Price consistency error');
        return { valid: false, reason: 'OHLC consistency error' };
      }
    }
    
    return { valid: true, timestamp: now };
  }
  
  /**
   * Verify indicator calculation
   */
  verifyIndicator(name, value, symbol) {
    if (typeof value !== 'number' || !isFinite(value)) {
      this.logRejection(symbol, 'indicator', `Invalid ${name} calculation`);
      return { valid: false, reason: `${name} is not a valid number` };
    }
    
    // RSI bounds check
    if (name === 'RSI' && (value < 0 || value > 100)) {
      this.logRejection(symbol, 'indicator', `RSI out of bounds: ${value}`);
      return { valid: false, reason: `RSI out of bounds: ${value}` };
    }
    
    return { valid: true, value };
  }
  
  logRejection(symbol, timeframe, reason) {
    this.rejectionLog.push({
      timestamp: new Date().toISOString(),
      symbol,
      timeframe,
      reason
    });
  }
  
  getTimeframeMs(tf) {
    const map = {
      '15m': 15 * 60 * 1000,
      '1h': 60 * 60 * 1000,
      '4h': 4 * 60 * 60 * 1000,
      '1d': 24 * 60 * 60 * 1000
    };
    return map[tf] || 60 * 60 * 1000;
  }
}

// ============================================
// TECHNICAL INDICATORS
// ============================================

class TechnicalIndicators {
  /**
   * Calculate EMA (Exponential Moving Average)
   */
  static ema(data, period) {
    const k = 2 / (period + 1);
    let ema = [data[0]];
    
    for (let i = 1; i < data.length; i++) {
      ema.push(data[i] * k + ema[i - 1] * (1 - k));
    }
    
    return ema;
  }
  
  /**
   * Calculate SMA (Simple Moving Average)
   */
  static sma(data, period) {
    const sma = [];
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) {
        sma.push(null);
      } else {
        const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
        sma.push(sum / period);
      }
    }
    return sma;
  }
  
  /**
   * Calculate RSI (Relative Strength Index)
   */
  static rsi(closes, period = 14) {
    const gains = [];
    const losses = [];
    
    for (let i = 1; i < closes.length; i++) {
      const change = closes[i] - closes[i - 1];
      gains.push(change > 0 ? change : 0);
      losses.push(change < 0 ? Math.abs(change) : 0);
    }
    
    const avgGains = this.sma(gains, period);
    const avgLosses = this.sma(losses, period);
    
    const rsi = [];
    for (let i = 0; i < avgGains.length; i++) {
      if (avgGains[i] === null || avgLosses[i] === null) {
        rsi.push(null);
      } else if (avgLosses[i] === 0) {
        rsi.push(100);
      } else {
        const rs = avgGains[i] / avgLosses[i];
        rsi.push(100 - (100 / (1 + rs)));
      }
    }
    
    return rsi;
  }
  
  /**
   * Calculate ATR (Average True Range)
   */
  static atr(highs, lows, closes, period = 14) {
    const tr = [];
    
    for (let i = 0; i < highs.length; i++) {
      if (i === 0) {
        tr.push(highs[i] - lows[i]);
      } else {
        const hl = highs[i] - lows[i];
        const hc = Math.abs(highs[i] - closes[i - 1]);
        const lc = Math.abs(lows[i] - closes[i - 1]);
        tr.push(Math.max(hl, hc, lc));
      }
    }
    
    return this.sma(tr, period);
  }
  
  /**
   * Calculate Bollinger Bands
   */
  static bollingerBands(closes, period = 20, stdDev = 2) {
    const sma = this.sma(closes, period);
    const bands = [];
    
    for (let i = 0; i < closes.length; i++) {
      if (sma[i] === null) {
        bands.push(null);
      } else {
        const slice = closes.slice(Math.max(0, i - period + 1), i + 1);
        const mean = sma[i];
        const variance = slice.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / slice.length;
        const std = Math.sqrt(variance);
        
        bands.push({
          upper: mean + stdDev * std,
          middle: mean,
          lower: mean - stdDev * std,
          width: (2 * stdDev * std) / mean * 100 // Width as percentage
        });
      }
    }
    
    return bands;
  }
  
  /**
   * Calculate MACD
   */
  static macd(closes, fast = 12, slow = 26, signal = 9) {
    const emaFast = this.ema(closes, fast);
    const emaSlow = this.ema(closes, slow);
    
    const macdLine = emaFast.map((f, i) => f - emaSlow[i]);
    const signalLine = this.ema(macdLine, signal);
    const histogram = macdLine.map((m, i) => m - signalLine[i]);
    
    return { macdLine, signalLine, histogram };
  }
  
  /**
   * Calculate Support/Resistance levels
   */
  static supportResistance(highs, lows, closes, lookback = 20) {
    const levels = [];
    
    // Find pivot highs and lows
    for (let i = 2; i < highs.length - 2; i++) {
      // Pivot high
      if (highs[i] > highs[i-1] && highs[i] > highs[i-2] && 
          highs[i] > highs[i+1] && highs[i] > highs[i+2]) {
        levels.push({ price: highs[i], type: 'resistance', strength: 1 });
      }
      
      // Pivot low
      if (lows[i] < lows[i-1] && lows[i] < lows[i-2] && 
          lows[i] < lows[i+1] && lows[i] < lows[i+2]) {
        levels.push({ price: lows[i], type: 'support', strength: 1 });
      }
    }
    
    // Cluster nearby levels
    const tolerance = 0.02; // 2% tolerance
    const clustered = [];
    
    for (const level of levels) {
      let found = false;
      for (const cluster of clustered) {
        if (Math.abs(cluster.price - level.price) / cluster.price < tolerance) {
          cluster.strength++;
          found = true;
          break;
        }
      }
      if (!found) {
        clustered.push({ ...level });
      }
    }
    
    // Sort by strength and recency
    return clustered
      .sort((a, b) => b.strength - a.strength)
      .slice(0, 10);
  }
}

// ============================================
// MARKET SCANNER
// ============================================

class MarketMatrix {
  constructor(config = CONFIG) {
    this.config = config;
    this.exchange = new ccxt[config.exchange]({
      enableRateLimit: true
    });
    this.radar = new RadarAgent();
    this.cache = new Map();
    this.macroBias = null;
  }
  
  /**
   * Fetch OHLCV data with Radar verification
   */
  async fetchOHLCV(symbol, timeframe, limit = 100) {
    try {
      const ohlcv = await this.exchange.fetchOHLCV(symbol, timeframe, undefined, limit);
      
      // Radar verification
      const verification = this.radar.verifyOHLCV(ohlcv, symbol, timeframe);
      
      if (!verification.valid) {
        console.error(`❌ RADAR REJECTION: ${symbol} ${timeframe} - ${verification.reason}`);
        return null;
      }
      
      // Cache verified data
      const key = `${symbol}:${timeframe}`;
      this.cache.set(key, {
        data: ohlcv,
        timestamp: verification.timestamp
      });
      
      return ohlcv;
    } catch (error) {
      console.error(`❌ Error fetching ${symbol} ${timeframe}:`, error.message);
      return null;
    }
  }
  
  /**
   * Parse OHLCV into structured data
   */
  parseOHLCV(ohlcv) {
    return {
      timestamps: ohlcv.map(c => c[0]),
      opens: ohlcv.map(c => c[1]),
      highs: ohlcv.map(c => c[2]),
      lows: ohlcv.map(c => c[3]),
      closes: ohlcv.map(c => c[4]),
      volumes: ohlcv.map(c => c[5])
    };
  }
  
  /**
   * Analyze a symbol across all timeframes
   */
  async analyzeSymbol(symbol) {
    const analysis = { symbol, timeframes: {}, verified: true };
    
    // Fetch all timeframes
    for (const [name, tf] of Object.entries(this.config.timeframes)) {
      const ohlcv = await this.fetchOHLCV(symbol, tf, 100);
      
      if (!ohlcv) {
        analysis.verified = false;
        continue;
      }
      
      const parsed = this.parseOHLCV(ohlcv);
      const lastIdx = parsed.closes.length - 1;
      
      // Calculate indicators
      const emaFast = TechnicalIndicators.ema(parsed.closes, this.config.indicators.emaFast);
      const emaSlow = TechnicalIndicators.ema(parsed.closes, this.config.indicators.emaSlow);
      const emaMacro = TechnicalIndicators.ema(parsed.closes, this.config.indicators.emaMacro);
      const rsi = TechnicalIndicators.rsi(parsed.closes, this.config.indicators.rsiPeriod);
      const atr = TechnicalIndicators.atr(parsed.highs, parsed.lows, parsed.closes, this.config.indicators.atrPeriod);
      const bb = TechnicalIndicators.bollingerBands(parsed.closes, this.config.indicators.bollingerPeriod, this.config.indicators.bollingerStdDev);
      const macd = TechnicalIndicators.macd(parsed.closes);
      const sr = TechnicalIndicators.supportResistance(parsed.highs, parsed.lows, parsed.closes);
      
      // Current values
      const currentPrice = parsed.closes[lastIdx];
      const prevPrice = parsed.closes[lastIdx - 1];
      const priceChange24h = ((currentPrice - parsed.closes[lastIdx - 24]) / parsed.closes[lastIdx - 24] * 100);
      
      // Trend determination
      const trend = this.determineTrend(currentPrice, emaFast[lastIdx], emaSlow[lastIdx], emaMacro[lastIdx]);
      
      // RSI condition
      const rsiValue = rsi[lastIdx];
      const rsiCondition = rsiValue > 70 ? 'OVERBOUGHT' : rsiValue < 30 ? 'OVERSOLD' : 'NEUTRAL';
      
      analysis.timeframes[name] = {
        timeframe: tf,
        price: currentPrice,
        priceChange24h,
        high24h: Math.max(...parsed.highs.slice(-24)),
        low24h: Math.min(...parsed.lows.slice(-24)),
        volume: parsed.volumes[lastIdx],
        avgVolume: parsed.volumes.slice(-20).reduce((a, b) => a + b, 0) / 20,
        
        // Trend
        trend: trend.direction,
        trendStrength: trend.strength,
        
        // Moving Averages
        emaFast: emaFast[lastIdx],
        emaSlow: emaSlow[lastIdx],
        emaMacro: emaMacro[lastIdx],
        
        // RSI
        rsi: rsiValue,
        rsiCondition,
        
        // ATR
        atr: atr[lastIdx],
        atrPercent: (atr[lastIdx] / currentPrice * 100),
        
        // Bollinger Bands
        bbUpper: bb[lastIdx]?.upper,
        bbMiddle: bb[lastIdx]?.middle,
        bbLower: bb[lastIdx]?.lower,
        bbWidth: bb[lastIdx]?.width,
        
        // MACD
        macdValue: macd.macdLine[lastIdx],
        macdSignal: macd.signalLine[lastIdx],
        macdHistogram: macd.histogram[lastIdx],
        
        // Support/Resistance
        nearestSupport: sr.find(l => l.type === 'support')?.price,
        nearestResistance: sr.find(l => l.type === 'resistance')?.price,
        levels: sr.slice(0, 5),
        
        // Timestamp
        timestamp: new Date(parsed.timestamps[lastIdx]).toISOString()
      };
    }
    
    return analysis;
  }
  
  /**
   * Determine trend direction and strength
   */
  determineTrend(price, emaFast, emaSlow, emaMacro) {
    let bullishSignals = 0;
    let bearishSignals = 0;
    
    // EMA alignment
    if (price > emaFast) bullishSignals++; else bearishSignals++;
    if (price > emaSlow) bullishSignals++; else bearishSignals++;
    if (price > emaMacro) bullishSignals++; else bearishSignals++;
    if (emaFast > emaSlow) bullishSignals++; else bearishSignals++;
    if (emaSlow > emaMacro) bullishSignals++; else bearishSignals++;
    
    const direction = bullishSignals > bearishSignals ? 'BULLISH' : 
                      bearishSignals > bullishSignals ? 'BEARISH' : 'RANGING';
    const strength = Math.abs(bullishSignals - bearishSignals) / 5;
    
    return { direction, strength };
  }
  
  /**
   * Generate confluence score (1-10)
   */
  calculateConfluence(analysis) {
    if (!analysis.verified) return 0;
    
    const tf = analysis.timeframes;
    let score = 0;
    let factors = [];
    
    // Daily trend (weight: 3)
    if (tf.daily?.trend === 'BULLISH') {
      score += 3;
      factors.push('Daily bullish');
    } else if (tf.daily?.trend === 'BEARISH') {
      score += 3;
      factors.push('Daily bearish');
    }
    
    // 4H alignment (weight: 2)
    if (tf.fourHour?.trend === tf.daily?.trend) {
      score += 2;
      factors.push('4H aligned');
    }
    
    // 1H alignment (weight: 2)
    if (tf.oneHour?.trend === tf.daily?.trend) {
      score += 2;
      factors.push('1H aligned');
    }
    
    // 15m setup (weight: 2)
    if (tf.fifteenMin?.rsiCondition === 'OVERSOLD' && tf.daily?.trend === 'BULLISH') {
      score += 2;
      factors.push('15m RSI oversold + daily bullish');
    } else if (tf.fifteenMin?.rsiCondition === 'OVERBOUGHT' && tf.daily?.trend === 'BEARISH') {
      score += 2;
      factors.push('15m RSI overbought + daily bearish');
    }
    
    // Bonus: Price near key levels
    const price = tf.fifteenMin?.price;
    const support = tf.daily?.nearestSupport;
    const resistance = tf.daily?.nearestResistance;
    
    if (support && price < support * 1.02) {
      score += 1;
      factors.push('Near support');
    }
    if (resistance && price > resistance * 0.98) {
      score += 1;
      factors.push('Near resistance');
    }
    
    return { score: Math.min(10, score), factors };
  }
  
  /**
   * Generate paper trade setup
   */
  generateTradeSetup(analysis, confluence) {
    if (confluence.score < 6) return null;
    
    const tf = analysis.timeframes;
    const price = tf.fifteenMin?.price;
    const atr = tf.fifteenMin?.atr;
    const trend = tf.daily?.trend;
    
    if (!price || !atr) return null;
    
    const side = trend === 'BULLISH' ? 'LONG' : 'SHORT';
    
    // Calculate levels based on ATR
    const riskMultiplier = 1.5;
    const rewardMultiplier = 3; // 2:1 R:R
    
    let entry, stopLoss, takeProfit;
    
    if (side === 'LONG') {
      entry = price;
      stopLoss = price - (atr * riskMultiplier);
      takeProfit = price + (atr * rewardMultiplier);
    } else {
      entry = price;
      stopLoss = price + (atr * riskMultiplier);
      takeProfit = price - (atr * rewardMultiplier);
    }
    
    const riskPercent = Math.abs((entry - stopLoss) / entry * 100);
    const rewardPercent = Math.abs((takeProfit - entry) / entry * 100);
    
    return {
      symbol: analysis.symbol,
      side,
      confluence: confluence.score,
      factors: confluence.factors,
      entry: entry.toFixed(8),
      stopLoss: stopLoss.toFixed(8),
      takeProfit: takeProfit.toFixed(8),
      riskPercent: riskPercent.toFixed(2),
      rewardPercent: rewardPercent.toFixed(2),
      riskRewardRatio: (rewardPercent / riskPercent).toFixed(2),
      timestamp: new Date().toISOString()
    };
  }
}

// ============================================
// REPORT GENERATORS
// ============================================

class ReportGenerator {
  constructor(matrix) {
    this.matrix = matrix;
  }
  
  /**
   * DAILY MACRO REPORT
   */
  async generateDailyReport() {
    console.log('\n' + '='.repeat(80));
    console.log('📊 DAILY MACRO REPORT');
    console.log(`Generated: ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}`);
    console.log('='.repeat(80) + '\n');
    
    const reports = [];
    
    for (const symbol of this.matrix.config.watchlist) {
      const analysis = await this.matrix.analyzeSymbol(symbol);
      
      if (!analysis.verified) {
        console.log(`⚠️ ${symbol}: Data verification failed`);
        continue;
      }
      
      const tf = analysis.timeframes.daily;
      const tf4h = analysis.timeframes.fourHour;
      
      console.log(`\n${'─'.repeat(40)}`);
      console.log(`💱 ${symbol}`);
      console.log(`${'─'.repeat(40)}`);
      console.log(`💰 Price: $${tf.price.toFixed(2)} (${tf.priceChange24h >= 0 ? '+' : ''}${tf.priceChange24h.toFixed(2)}% 24h)`);
      console.log(`📈 Range: $${tf.low24h.toFixed(2)} - $${tf.high24h.toFixed(2)}`);
      console.log(`🎯 Trend: ${tf.trend} (Strength: ${(tf.trendStrength * 100).toFixed(0)}%)`);
      console.log(`📊 RSI: ${tf.rsi.toFixed(1)} (${tf.rsiCondition})`);
      console.log(`📏 ATR: $${tf.atr?.toFixed(2)} (${tf.atrPercent?.toFixed(2)}%)`);
      console.log(`📐 EMA9: $${tf.emaFast?.toFixed(2)} | EMA21: $${tf.emaSlow?.toFixed(2)} | EMA50: $${tf.emaMacro?.toFixed(2)}`);
      console.log(`🛡️ Support: $${tf.nearestSupport?.toFixed(2)} | Resistance: $${tf.nearestResistance?.toFixed(2)}`);
      console.log(`📦 Volume: ${(tf.volume / 1e6).toFixed(2)}M (Avg: ${(tf.avgVolume / 1e6).toFixed(2)}M)`);
      
      // Macro bias
      let bias = 'NEUTRAL';
      if (tf.trend === 'BULLISH' && tf.rsi < 70 && tf.trendStrength > 0.6) {
        bias = 'BULLISH_BIAS';
      } else if (tf.trend === 'BEARISH' && tf.rsi > 30 && tf.trendStrength > 0.6) {
        bias = 'BEARISH_BIAS';
      } else if (tf.rsiCondition === 'OVERBOUGHT') {
        bias = 'CAUTION_LONGS';
      } else if (tf.rsiCondition === 'OVERSOLD') {
        bias = 'CAUTION_SHORTS';
      }
      
      console.log(`🎯 MACRO BIAS: ${bias}`);
      
      reports.push({
        symbol,
        price: tf.price,
        change24h: tf.priceChange24h,
        trend: tf.trend,
        rsi: tf.rsi,
        bias
      });
      
      // Store macro bias
      this.matrix.macroBias = {
        symbol,
        trend: tf.trend,
        bias,
        timestamp: new Date().toISOString()
      };
    }
    
    // Save report
    this.saveReport('daily-macro', reports);
    
    console.log('\n' + '='.repeat(80));
    console.log('✅ Daily Macro Report Complete');
    console.log('='.repeat(80) + '\n');
    
    return reports;
  }
  
  /**
   * 4-HOUR OUTLOOK MONITOR
   */
  async generate4HourReport() {
    console.log('\n' + '='.repeat(80));
    console.log('⏰ 4-HOUR OUTLOOK MONITOR');
    console.log(`Generated: ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}`);
    console.log('='.repeat(80) + '\n');
    
    const alerts = [];
    
    for (const symbol of this.matrix.config.watchlist) {
      const analysis = await this.matrix.analyzeSymbol(symbol);
      
      if (!analysis.verified) continue;
      
      const tf4h = analysis.timeframes.fourHour;
      const tfDaily = analysis.timeframes.daily;
      
      // Check for alignment with daily bias
      const aligned = tf4h.trend === tfDaily.trend;
      
      // Check for momentum changes
      const macdDivergence = tf4h.macdHistogram < 0 && tfDaily.trend === 'BULLISH' ||
                             tf4h.macdHistogram > 0 && tfDaily.trend === 'BEARISH';
      
      // Check for breakout
      const price = tf4h.price;
      const nearResistance = tf4h.nearestResistance && price > tf4h.nearestResistance * 0.99;
      const nearSupport = tf4h.nearestSupport && price < tf4h.nearestSupport * 1.01;
      
      if (aligned || macdDivergence || nearResistance || nearSupport) {
        let message = `💱 ${symbol}: `;
        const reasons = [];
        
        if (aligned) reasons.push(`4H aligned with Daily ${tfDaily.trend}`);
        if (macdDivergence) reasons.push('MACD divergence detected');
        if (nearResistance) reasons.push('Testing resistance');
        if (nearSupport) reasons.push('Testing support');
        
        message += reasons.join(' | ');
        console.log(message);
        
        alerts.push({
          symbol,
          trend4h: tf4h.trend,
          trendDaily: tfDaily.trend,
          aligned,
          macdDivergence,
          nearResistance,
          nearSupport,
          price: tf4h.price
        });
      }
    }
    
    if (alerts.length === 0) {
      console.log('✅ No significant 4H changes detected');
    }
    
    this.saveReport('4h-outlook', alerts);
    return alerts;
  }
  
  /**
   * 1-HOUR SHIFT MONITOR
   */
  async generate1HourReport() {
    console.log('\n' + '='.repeat(80));
    console.log('🕐 1-HOUR SHIFT MONITOR');
    console.log(`Generated: ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}`);
    console.log('='.repeat(80) + '\n');
    
    const alerts = [];
    
    for (const symbol of this.matrix.config.watchlist) {
      const analysis = await this.matrix.analyzeSymbol(symbol);
      
      if (!analysis.verified) continue;
      
      const tf1h = analysis.timeframes.oneHour;
      const tf4h = analysis.timeframes.fourHour;
      
      // Volume spike detection
      const volumeSpike = tf1h.volume > tf1h.avgVolume * 2;
      
      // Support/Resistance break
      const supportBreak = tf1h.price < tf1h.nearestSupport * 0.99;
      const resistanceBreak = tf1h.price > tf1h.nearestResistance * 1.01;
      
      // Trend exhaustion (RSI extreme against trend)
      const exhaustion = (tf4h.trend === 'BULLISH' && tf1h.rsi > 75) ||
                         (tf4h.trend === 'BEARISH' && tf1h.rsi < 25);
      
      if (volumeSpike || supportBreak || resistanceBreak || exhaustion) {
        let message = `💱 ${symbol}: `;
        const reasons = [];
        
        if (volumeSpike) reasons.push(`Volume spike (${(tf1h.volume / 1e6).toFixed(1)}M vs ${(tf1h.avgVolume / 1e6).toFixed(1)}M avg)`);
        if (supportBreak) reasons.push('🔴 Support break');
        if (resistanceBreak) reasons.push('🟢 Resistance break');
        if (exhaustion) reasons.push(`⚠️ Trend exhaustion (RSI: ${tf1h.rsi.toFixed(1)})`);
        
        message += reasons.join(' | ');
        console.log(message);
        
        alerts.push({
          symbol,
          volumeSpike,
          supportBreak,
          resistanceBreak,
          exhaustion,
          price: tf1h.price,
          rsi: tf1h.rsi
        });
      }
    }
    
    if (alerts.length === 0) {
      console.log('✅ No 1H shifts detected - logging internally');
    }
    
    this.saveReport('1h-shift', alerts, alerts.length === 0);
    return alerts;
  }
  
  /**
   * 15-MINUTE TACTICAL SCANNER
   */
  async generate15MinReport() {
    console.log('\n' + '='.repeat(80));
    console.log('⚡ 15-MINUTE TACTICAL SCANNER');
    console.log(`Generated: ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}`);
    console.log('='.repeat(80) + '\n');
    
    const signals = [];
    
    for (const symbol of this.matrix.config.watchlist) {
      const analysis = await this.matrix.analyzeSymbol(symbol);
      
      if (!analysis.verified) continue;
      
      // Calculate confluence
      const confluence = this.matrix.calculateConfluence(analysis);
      
      // Only alert on high probability setups
      if (confluence.score >= 6) {
        const trade = this.matrix.generateTradeSetup(analysis, confluence);
        
        if (trade) {
          console.log('🚨 ACTIONABLE SIGNAL DETECTED');
          console.log(`${'─'.repeat(40)}`);
          console.log(`💱 ${trade.symbol}`);
          console.log(`📈 Side: ${trade.side}`);
          console.log(`🎯 Confluence Score: ${trade.confluence}/10`);
          console.log(`📊 Factors: ${trade.factors.join(', ')}`);
          console.log(`📍 Entry: $${trade.entry}`);
          console.log(`🛡️ Stop Loss: $${trade.stopLoss} (${trade.riskPercent}%)`);
          console.log(`🎯 Take Profit: $${trade.takeProfit} (${trade.rewardPercent}%)`);
          console.log(`📊 R:R Ratio: ${trade.riskRewardRatio}`);
          console.log(`${'─'.repeat(40)}\n`);
          
          signals.push(trade);
        }
      }
    }
    
    if (signals.length === 0) {
      console.log('✅ No high-probability setups at this time');
    } else {
      console.log(`\n📌 ${signals.length} potential trade(s) identified`);
      console.log('⚠️ PAPER TRADING ONLY - Human confirmation required\n');
    }
    
    this.saveReport('15m-tactical', signals);
    return signals;
  }
  
  /**
   * Save report to file
   */
  saveReport(type, data, silent = false) {
    const dir = this.matrix.config.outputDir;
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${type}-${timestamp}.json`;
    const filepath = path.join(dir, filename);
    
    fs.writeFileSync(filepath, JSON.stringify({
      type,
      timestamp: new Date().toISOString(),
      data
    }, null, 2));
    
    if (!silent && data.length > 0) {
      console.log(`📁 Report saved: ${filename}`);
    }
  }
}

// ============================================
// CLI ENTRY POINT
// ============================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  
  const matrix = new MarketMatrix();
  const reporter = new ReportGenerator(matrix);
  
  switch (command) {
    case 'daily':
      await reporter.generateDailyReport();
      break;
      
    case '4h':
      await reporter.generate4HourReport();
      break;
      
    case '1h':
      await reporter.generate1HourReport();
      break;
      
    case '15m':
      await reporter.generate15MinReport();
      break;
      
    case 'scan':
      // Run all reports
      await reporter.generateDailyReport();
      await reporter.generate4HourReport();
      await reporter.generate1HourReport();
      await reporter.generate15MinReport();
      break;
      
    case 'analyze':
      const symbol = args[1] || 'BTC/USDT';
      const analysis = await matrix.analyzeSymbol(symbol);
      console.log(JSON.stringify(analysis, null, 2));
      break;
      
    case 'test':
      // Test CCXT connection
      console.log('Testing CCXT connection...');
      const ohlcv = await matrix.fetchOHLCV('BTC/USDT', '1d', 10);
      if (ohlcv) {
        console.log('✅ CCXT working! Latest BTC price:', ohlcv[ohlcv.length - 1][4]);
      } else {
        console.log('❌ CCXT connection failed');
      }
      break;
      
    default:
      console.log(`
Multi-Timeframe Market Matrix

Usage:
  node market-matrix.js daily    - Generate Daily Macro Report
  node market-matrix.js 4h       - Generate 4-Hour Outlook Monitor
  node market-matrix.js 1h       - Generate 1-Hour Shift Monitor
  node market-matrix.js 15m      - Generate 15-Min Tactical Scanner
  node market-matrix.js scan     - Run all reports
  node market-matrix.js analyze [SYMBOL]  - Analyze specific symbol
  node market-matrix.js test     - Test CCXT connection
      `);
  }
}

main().catch(console.error);

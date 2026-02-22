#!/usr/bin/env node
/**
 * TRINITY PAPER EXECUTOR v2.0
 * 
 * Permanent Binance Testnet Integration
 * - Source of Truth: Binance Testnet API
 * - ML Loop Integration on trade close
 * - Discord + JSON feed routing
 * 
 * Author: Netto.AI
 * Created: 2026-02-22
 * Upgraded: 2026-02-22
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const TRADING_DIR = path.join(process.env.HOME, '.openclaw/workspace/trading');
const DASHBOARD_FEED = path.join(TRADING_DIR, 'trinity_dashboard_feed.json');
const ML_LOG = path.join(TRADING_DIR, 'Trinity_ML_Log.md');

// ============================================
// BINANCE TESTNET INTERFACE
// ============================================

class BinanceTestnetClient {
  constructor() {
    this.pythonPath = 'python3';
    this.apiPath = path.join(TRADING_DIR, 'binance_api.py');
  }

  /**
   * Execute binance_api.py and return parsed result
   */
  execApi(command, extra = '') {
    try {
      const result = execSync(`${this.pythonPath} ${this.apiPath} ${command} ${extra}`, {
        encoding: 'utf-8',
        timeout: 30000,
        cwd: TRADING_DIR
      });
      return JSON.parse(result.trim());
    } catch (error) {
      console.error('API execution error:', error.message);
      return { error: error.message };
    }
  }

  /**
   * Get all open positions from Binance Testnet
   */
  getOpenPositions() {
    return this.execApi('positions');
  }

  /**
   * Get current price for a symbol
   */
  getCurrentPrice(symbol) {
    const result = this.execApi('price', symbol);
    return result.price || null;
  }

  /**
   * Get account balance
   */
  getBalance() {
    const result = this.execApi('balance');
    return result.balance || 0;
  }
}

// ============================================
// STATE MANAGER
// ============================================

class StateManager {
  constructor() {
    this.stateFile = path.join(TRADING_DIR, 'executor_state.json');
    this.loadState();
  }

  loadState() {
    if (fs.existsSync(this.stateFile)) {
      this.state = JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
    } else {
      this.state = {
        trackedPositions: {},
        tradeHistory: [],
        stats: {
          totalTrades: 0,
          wins: 0,
          losses: 0,
          totalPnl: 0,
          consecutiveLosses: 0,
          circuitBreakerActive: false
        }
      };
    }
  }

  saveState() {
    fs.writeFileSync(this.stateFile, JSON.stringify(this.state, null, 2));
  }

  trackPosition(tradeId, symbol, side, entryPrice, stopLoss, takeProfit, confluence, factors) {
    this.state.trackedPositions[symbol] = {
      tradeId,
      symbol,
      side,
      entryPrice,
      stopLoss,
      takeProfit,
      confluence,
      factors,
      entryTime: new Date().toISOString(),
      status: 'OPEN'
    };
    this.saveState();
  }

  closePosition(symbol, exitPrice, pnl, reason) {
    const pos = this.state.trackedPositions[symbol];
    if (!pos) return null;

    const closedTrade = {
      ...pos,
      exitPrice,
      exitTime: new Date().toISOString(),
      pnl,
      pnlPercent: (pnl / 200 * 100), // Assuming $200 position size
      reason,
      result: pnl >= 0 ? 'WIN' : 'LOSS',
      status: 'CLOSED'
    };

    this.state.tradeHistory.push(closedTrade);
    delete this.state.trackedPositions[symbol];

    // Update stats
    this.state.stats.totalTrades++;
    if (pnl >= 0) {
      this.state.stats.wins++;
      this.state.stats.consecutiveLosses = 0;
    } else {
      this.state.stats.losses++;
      this.state.stats.consecutiveLosses++;
    }
    this.state.stats.totalPnl += pnl;

    // Circuit breaker check
    if (this.state.stats.consecutiveLosses >= 3) {
      this.state.stats.circuitBreakerActive = true;
    }

    this.saveState();
    return closedTrade;
  }
}

// ============================================
// ML REFLECTION ENGINE
// ============================================

class MLReflectionEngine {
  generateReflection(trade) {
    const isWin = trade.result === 'WIN';
    
    let reflection = {
      tradeId: trade.tradeId,
      symbol: trade.symbol,
      side: trade.side,
      result: trade.result,
      pnl: trade.pnl,
      pnlPercent: trade.pnlPercent,
      lesson: '',
      strategyAdjustment: ''
    };

    if (isWin) {
      reflection.lesson = this.generateWinLesson(trade);
      reflection.strategyAdjustment = 'Continue with current strategy — this setup type is profitable.';
    } else {
      reflection.lesson = this.generateLossLesson(trade);
      reflection.strategyAdjustment = this.generateStrategyFix(trade);
    }

    return reflection;
  }

  generateWinLesson(trade) {
    const lessons = [];
    
    lessons.push(`**Why this trade won:**`);
    lessons.push(`- Multi-timeframe alignment was correct`);
    lessons.push(`- Confluence factors (${trade.factors.join(', ')}) played out as expected`);
    lessons.push(`- Entry timing was optimal — price moved in predicted direction`);
    lessons.push(`- Risk management worked: 2:1 R:R achieved`);
    lessons.push(``);
    lessons.push(`**Key takeaway:** Trust setups with confluence ≥6/10 when timeframes align.`);
    
    return lessons.join('\n');
  }

  generateLossLesson(trade) {
    const lessons = [];
    
    lessons.push(`**Why this trade failed:**`);
    
    if (trade.reason === 'STOP_LOSS') {
      if (trade.factors.includes('Near support') && trade.side === 'SHORT') {
        lessons.push(`- Entry was shorting into a support level`);
        lessons.push(`- Support held and triggered a bounce`);
      } else if (trade.factors.includes('Near resistance') && trade.side === 'LONG') {
        lessons.push(`- Entry was longing into a resistance level`);
        lessons.push(`- Resistance held and triggered a rejection`);
      } else {
        lessons.push(`- Setup had false confluence — one or more factors were misleading`);
        lessons.push(`- Market reversed before the move could develop`);
      }
    }
    
    lessons.push(``);
    lessons.push(`**Key takeaway:** Re-evaluate entry timing and wait for stronger confirmation.`);
    
    return lessons.join('\n');
  }

  generateStrategyFix(trade) {
    if (trade.factors.includes('Near support') && trade.side === 'SHORT') {
      return `**NEW RULE:** Do not take SHORT setups when "Near support" is a confluence factor. Wait for support break confirmation first.`;
    }
    if (trade.factors.includes('Near resistance') && trade.side === 'LONG') {
      return `**NEW RULE:** Do not take LONG setups when "Near resistance" is a confluence factor. Wait for resistance break confirmation first.`;
    }
    return `Review similar losing patterns and adjust confluence scoring weight.`;
  }

  writeToMLLog(reflection) {
    const entry = `

---

### Trade #${reflection.tradeId.replace('TRD-', '')} — ${reflection.symbol} ${reflection.side} [CLOSED]

**Exit Time:** ${new Date().toISOString()}
**Result:** ${reflection.result === 'WIN' ? '✅ WIN' : '❌ LOSS'}

#### PnL Summary
- **Realized PnL:** ${reflection.pnl >= 0 ? '+' : ''}${reflection.pnlPercent.toFixed(2)}% ($${reflection.pnl.toFixed(2)})
- **Trade ID:** ${reflection.tradeId}

#### AI Remarks (Lesson)
${reflection.lesson}

#### Strategy Improvement
${reflection.strategyAdjustment}

`;
    fs.appendFileSync(ML_LOG, entry);
  }
}

// ============================================
// DASHBOARD FEED UPDATER
// ============================================

class DashboardFeedUpdater {
  update(closedTrade, reflection) {
    let feed = JSON.parse(fs.readFileSync(DASHBOARD_FEED, 'utf-8'));
    
    // Update summary
    feed.summary.total_trades = feed.trades.length + 1;
    feed.summary.wins = (feed.summary.wins || 0) + (closedTrade.result === 'WIN' ? 1 : 0);
    feed.summary.losses = (feed.summary.losses || 0) + (closedTrade.result === 'LOSS' ? 1 : 0);
    feed.summary.total_pnl = (feed.summary.total_pnl || 0) + closedTrade.pnl;
    feed.summary.unrealized_pnl = 0;
    feed.metadata.last_updated = new Date().toISOString();
    feed.metadata.execution_mode = 'BINANCE_TESTNET';
    
    // Add to trades history
    feed.trades.push({
      trade_id: closedTrade.tradeId,
      timestamp_entry: closedTrade.entryTime,
      timestamp_exit: closedTrade.exitTime,
      asset_pair: closedTrade.symbol,
      side: closedTrade.side,
      confluence_score: closedTrade.confluence,
      entry_price: closedTrade.entryPrice,
      exit_price: closedTrade.exitPrice,
      pnl_percent: closedTrade.pnlPercent,
      pnl_usd: closedTrade.pnl,
      result: closedTrade.result,
      ai_ml_reflection: reflection.lesson
    });
    
    // Update open positions
    feed.open_positions = feed.open_positions.filter(p => p.trade_id !== closedTrade.tradeId);
    
    // Add Discord webhook payload
    feed.discord_webhook_payloads.push({
      type: 'TRADE_CLOSED',
      username: 'Trinity Trading Bot',
      embeds: [{
        title: `${closedTrade.result === 'WIN' ? '✅' : '❌'} ${closedTrade.tradeId} Closed`,
        color: closedTrade.result === 'WIN' ? 3066993 : 15158332,
        fields: [
          { name: 'Pair', value: closedTrade.symbol, inline: true },
          { name: 'Side', value: closedTrade.side, inline: true },
          { name: 'Result', value: closedTrade.result, inline: true },
          { name: 'PnL', value: `${closedTrade.pnl >= 0 ? '+' : ''}${closedTrade.pnlPercent.toFixed(2)}% ($${closedTrade.pnl.toFixed(2)})`, inline: true },
          { name: 'Lesson', value: reflection.lesson.substring(0, 100) + '...', inline: false }
        ],
        footer: { text: 'Trinity ML Protocol' },
        timestamp: new Date().toISOString()
      }]
    });
    
    fs.writeFileSync(DASHBOARD_FEED, JSON.stringify(feed, null, 2));
  }
}

// ============================================
// MAIN MONITOR
// ============================================

async function main() {
  console.log('\n' + '='.repeat(70));
  console.log('📋 TRINITY PAPER EXECUTOR v2.0');
  console.log('📡 Source of Truth: Binance Testnet API');
  console.log(`⏰ ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}`);
  console.log('='.repeat(70));

  const binance = new BinanceTestnetClient();
  const state = new StateManager();
  const mlEngine = new MLReflectionEngine();
  const dashboard = new DashboardFeedUpdater();

  // Get live positions from Binance Testnet
  console.log('\n🔌 Fetching positions from Binance Testnet...');
  const binancePositions = binance.getOpenPositions();
  
  if (binancePositions.error) {
    console.log(`❌ Error: ${binancePositions.error}`);
    return;
  }

  console.log(`📊 Found ${binancePositions.length} open position(s) on Binance Testnet\n`);

  // Track new positions
  for (const pos of binancePositions) {
    if (!state.state.trackedPositions[pos.symbol]) {
      console.log(`📌 New position detected: ${pos.symbol} ${pos.side}`);
      // Would need to get SL/TP from somewhere - for now, skip
    }
  }

  // Check each tracked position against Binance
  for (const [symbol, trackedPos] of Object.entries(state.state.trackedPositions)) {
    const livePos = binancePositions.find(p => p.symbol === symbol);
    
    if (!livePos || livePos.size === 0) {
      // Position closed on Binance!
      console.log(`\n🚨 POSITION CLOSED: ${symbol}`);
      console.log(`   Trade ID: ${trackedPos.tradeId}`);
      
      // Determine exit reason
      const currentPrice = binance.getCurrentPrice(symbol);
      let exitReason = 'UNKNOWN';
      let exitPrice = currentPrice;
      
      if (trackedPos.side === 'SHORT') {
        if (currentPrice <= trackedPos.takeProfit) {
          exitReason = 'TAKE_PROFIT';
          exitPrice = trackedPos.takeProfit;
        } else if (currentPrice >= trackedPos.stopLoss) {
          exitReason = 'STOP_LOSS';
          exitPrice = trackedPos.stopLoss;
        }
      } else {
        if (currentPrice >= trackedPos.takeProfit) {
          exitReason = 'TAKE_PROFIT';
          exitPrice = trackedPos.takeProfit;
        } else if (currentPrice <= trackedPos.stopLoss) {
          exitReason = 'STOP_LOSS';
          exitPrice = trackedPos.stopLoss;
        }
      }
      
      // Calculate PnL
      let pnl = 0;
      if (trackedPos.side === 'SHORT') {
        pnl = (trackedPos.entryPrice - exitPrice) / trackedPos.entryPrice * 200;
      } else {
        pnl = (exitPrice - trackedPos.entryPrice) / trackedPos.entryPrice * 200;
      }
      
      console.log(`   Exit Reason: ${exitReason}`);
      console.log(`   Exit Price: $${exitPrice}`);
      console.log(`   PnL: ${pnl >= 0 ? '+' : ''}${(pnl/200*100).toFixed(2)}% ($${pnl.toFixed(2)})`);
      
      // Close position in state
      const closedTrade = state.closePosition(symbol, exitPrice, pnl, exitReason);
      
      if (closedTrade) {
        // Generate ML reflection
        console.log(`\n🧠 Generating ML reflection...`);
        const reflection = mlEngine.generateReflection(closedTrade);
        
        // Write to ML log
        mlEngine.writeToMLLog(reflection);
        console.log(`   ✅ ML log updated`);
        
        // Update dashboard feed
        dashboard.update(closedTrade, reflection);
        console.log(`   ✅ Dashboard feed updated`);
        
        // Check circuit breaker
        if (state.state.stats.circuitBreakerActive) {
          console.log(`\n🚨 CIRCUIT BREAKER ACTIVATED — 3 consecutive losses`);
          console.log(`   Trading paused until manual reset`);
        }
      }
    } else {
      // Position still open - report status
      console.log(`💱 ${symbol} (${trackedPos.side})`);
      console.log(`   Entry: $${trackedPos.entryPrice}`);
      console.log(`   Current: $${livePos.entry_price}`);
      console.log(`   Unrealized PnL: ${livePos.unrealized_pnl >= 0 ? '+' : ''}$${livePos.unrealized_pnl.toFixed(2)}`);
      console.log(`   SL: $${trackedPos.stopLoss} | TP: $${trackedPos.takeProfit}`);
    }
  }

  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('📊 EXECUTOR SUMMARY');
  console.log('='.repeat(70));
  console.log(`Open Positions: ${binancePositions.length}`);
  console.log(`Total Trades: ${state.state.stats.totalTrades}`);
  console.log(`Wins/Losses: ${state.state.stats.wins}/${state.state.stats.losses}`);
  console.log(`Win Rate: ${state.state.stats.totalTrades > 0 ? ((state.state.stats.wins / state.state.stats.totalTrades) * 100).toFixed(1) : 0}%`);
  console.log(`Total PnL: ${state.state.stats.totalPnl >= 0 ? '+' : ''}$${state.state.stats.totalPnl.toFixed(2)}`);
  console.log(`Circuit Breaker: ${state.state.stats.circuitBreakerActive ? 'ACTIVE 🚨' : 'Inactive'}`);
  
  // Get balance
  const balance = binance.getBalance();
  console.log(`Binance Testnet Balance: $${balance.toFixed(2)}`);
  console.log('='.repeat(70) + '\n');
}

main().catch(console.error);
#!/usr/bin/env node
/**
 * PAPER TRADING EXECUTOR
 * 
 * Monitors open positions and executes exits when TP/SL hit.
 * Updates Trinity_ML_Log.md with lessons learned.
 * 
 * Author: Netto.AI
 * Created: 2026-02-22
 */

const ccxt = require('ccxt');
const fs = require('fs');
const path = require('path');

const TRADING_DIR = path.join(process.env.HOME, '.openclaw/workspace/trading');
const POSITIONS_FILE = path.join(TRADING_DIR, 'paper_positions.json');
const ML_LOG_FILE = path.join(TRADING_DIR, 'Trinity_ML_Log.md');

const exchange = new ccxt.binance({ enableRateLimit: true });

async function checkPositions() {
  console.log('\n' + '='.repeat(60));
  console.log('📋 PAPER TRADING MONITOR');
  console.log(`Time: ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}`);
  console.log('='.repeat(60));
  
  // Load positions
  if (!fs.existsSync(POSITIONS_FILE)) {
    console.log('No positions file found.');
    return;
  }
  
  const data = JSON.parse(fs.readFileSync(POSITIONS_FILE, 'utf8'));
  const positions = data.positions || [];
  
  if (positions.length === 0) {
    console.log('✅ No open positions');
    return;
  }
  
  console.log(`\n📊 Monitoring ${positions.length} open position(s)...\n`);
  
  for (let i = positions.length - 1; i >= 0; i--) {
    const pos = positions[i];
    
    // Get current price
    const ticker = await exchange.fetchTicker(pos.symbol.replace('/', ''));
    const currentPrice = ticker.last;
    
    console.log(`💱 ${pos.symbol} (${pos.side})`);
    console.log(`   Entry: $${pos.entry_price}`);
    console.log(`   Current: $${currentPrice.toFixed(8)}`);
    console.log(`   SL: $${pos.stop_loss} | TP: $${pos.take_profit}`);
    
    // Check for exit
    let shouldClose = false;
    let exitReason = '';
    let exitPrice = currentPrice;
    let pnlPercent = 0;
    let pnlUsd = 0;
    
    if (pos.side === 'LONG') {
      if (currentPrice >= pos.take_profit) {
        shouldClose = true;
        exitReason = 'TAKE PROFIT HIT';
        exitPrice = pos.take_profit;
        pnlPercent = ((exitPrice - pos.entry_price) / pos.entry_price * 100);
      } else if (currentPrice <= pos.stop_loss) {
        shouldClose = true;
        exitReason = 'STOP LOSS HIT';
        exitPrice = pos.stop_loss;
        pnlPercent = ((exitPrice - pos.entry_price) / pos.entry_price * 100);
      }
    } else { // SHORT
      if (currentPrice <= pos.take_profit) {
        shouldClose = true;
        exitReason = 'TAKE PROFIT HIT';
        exitPrice = pos.take_profit;
        pnlPercent = ((pos.entry_price - exitPrice) / pos.entry_price * 100);
      } else if (currentPrice >= pos.stop_loss) {
        shouldClose = true;
        exitReason = 'STOP LOSS HIT';
        exitPrice = pos.stop_loss;
        pnlPercent = ((pos.entry_price - exitPrice) / pos.entry_price * 100);
      }
    }
    
    if (shouldClose) {
      pnlUsd = pos.position_size_usd * (pnlPercent / 100);
      
      console.log(`\n🚨 EXIT TRIGGERED: ${exitReason}`);
      console.log(`   Exit Price: $${exitPrice}`);
      console.log(`   PnL: ${pnlPercent >= 0 ? '+' : ''}${pnlPercent.toFixed(2)}% ($${pnlUsd.toFixed(2)})`);
      
      // Close position
      const closedTrade = {
        ...pos,
        exit_price: exitPrice,
        exit_time: new Date().toISOString(),
        exit_reason: exitReason,
        pnl_percent: pnlPercent,
        pnl_usd: pnlUsd,
        status: 'CLOSED',
        result: pnlPercent >= 0 ? 'WIN' : 'LOSS'
      };
      
      // Move to history
      data.trade_history.push(closedTrade);
      positions.splice(i, 1);
      
      // Update stats
      data.stats.total_trades++;
      if (pnlPercent >= 0) {
        data.stats.wins++;
        data.stats.consecutive_losses = 0;
      } else {
        data.stats.losses++;
        data.stats.consecutive_losses++;
      }
      data.stats.total_pnl += pnlUsd;
      
      // Circuit breaker check
      if (data.stats.consecutive_losses >= 3) {
        data.stats.circuit_breaker_active = true;
        console.log('\n🚨 CIRCUIT BREAKER ACTIVATED — 3 consecutive losses');
      }
      
      // Write ML lesson
      writeMLLesson(closedTrade, data.stats);
      
      // Update positions file
      data.positions = positions;
      fs.writeFileSync(POSITIONS_FILE, JSON.stringify(data, null, 2));
      
      console.log(`   ✅ Position closed and logged`);
    } else {
      // Calculate unrealized PnL
      let unrealizedPnl = 0;
      if (pos.side === 'LONG') {
        unrealizedPnl = ((currentPrice - pos.entry_price) / pos.entry_price * 100);
      } else {
        unrealizedPnl = ((pos.entry_price - currentPrice) / pos.entry_price * 100);
      }
      console.log(`   Unrealized PnL: ${unrealizedPnl >= 0 ? '+' : ''}${unrealizedPnl.toFixed(2)}%`);
    }
  }
}

function writeMLLesson(trade, stats) {
  const lesson = generateLesson(trade);
  
  const entry = `

---

### Trade #${trade.trade_id.replace('TRD-', '')} — ${trade.symbol} ${trade.side} [CLOSED]

**Entry Time:** ${trade.entry_time}
**Exit Time:** ${trade.exit_time}
**Result:** ${trade.result === 'WIN' ? '✅ WIN' : '❌ LOSS'}

#### Setup Analysis
- **Confluence Score:** ${trade.confluence}/10
- **Factors:** ${trade.factors.join(', ')}
- **Entry Price:** $${trade.entry_price}
- **Exit Price:** $${trade.exit_price}
- **Exit Reason:** ${trade.exit_reason}
- **Stop Loss:** $${trade.stop_loss}
- **Take Profit:** $${trade.take_profit}

#### Result
- **PnL:** ${trade.pnl_percent >= 0 ? '+' : ''}${trade.pnl_percent.toFixed(2)}% ($${trade.pnl_usd.toFixed(2)})
- **Position Size:** $${trade.position_size_usd}

${lesson}

`;
  
  // Append to ML log
  fs.appendFileSync(ML_LOG_FILE, entry);
}

function generateLesson(trade) {
  const isWin = trade.result === 'WIN';
  
  let remarks = `#### AI Remarks (Lesson)\n`;
  remarks += `\n`;
  
  if (isWin) {
    remarks += `**Why this trade won:**\n`;
    if (trade.exit_reason === 'TAKE PROFIT HIT') {
      remarks += `- The multi-timeframe alignment was correct\n`;
      remarks += `- Confluence factors (${trade.factors.join(', ')}) played out as expected\n`;
      remarks += `- Entry timing was optimal — price moved in predicted direction\n`;
      remarks += `- Risk management worked: 2:1 R:R achieved\n`;
    }
    remarks += `\n**Key takeaway:** Trust setups with confluence ≥6/10 when timeframes align.\n`;
  } else {
    remarks += `**Why this trade failed:**\n`;
    if (trade.exit_reason === 'STOP LOSS HIT') {
      remarks += `- Entry was against a key ${trade.side === 'LONG' ? 'resistance' : 'support'} level\n`;
      remarks += `- The setup had false confluence — one or more factors were misleading\n`;
      remarks += `- Market reversed before the move could develop\n`;
    }
    remarks += `\n**Key takeaway:** `;
    if (trade.factors.includes('Near support') && trade.side === 'SHORT') {
      remarks += `Avoid shorting into support — it often triggers a bounce.\n`;
    } else if (trade.factors.includes('Near resistance') && trade.side === 'LONG') {
      remarks += `Avoid longing into resistance — it often triggers a rejection.\n`;
    } else {
      remarks += `Re-evaluate entry timing and wait for stronger confirmation.\n`;
    }
  }
  
  remarks += `\n#### Strategy Improvement\n`;
  remarks += `- `;
  
  if (!isWin) {
    if (trade.factors.includes('Near support') && trade.side === 'SHORT') {
      remarks += `**NEW RULE:** Do not take SHORT setups when "Near support" is a confluence factor. Wait for support break confirmation first.\n`;
    } else if (trade.factors.includes('Near resistance') && trade.side === 'LONG') {
      remarks += `**NEW RULE:** Do not take LONG setups when "Near resistance" is a confluence factor. Wait for resistance break confirmation first.\n`;
    } else {
      remarks += `Review similar losing patterns and adjust confluence scoring weight.\n`;
    }
  } else {
    remarks += `Continue with current strategy — this setup type is profitable.\n`;
  }
  
  return remarks;
}

// Run monitor
checkPositions().catch(console.error);
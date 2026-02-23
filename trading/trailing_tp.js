#!/usr/bin/env node
/**
 * TRAILING TAKE PROFIT MODULE
 * 
 * For SHORT positions:
 * - Trail TP follows price DOWN (favorable direction)
 * - If price reverses UP by trail_percent, close position
 * 
 * For LONG positions:
 * - Trail TP follows price UP (favorable direction)
 * - If price reverses DOWN by trail_percent, close position
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const TRADING_DIR = path.join(process.env.HOME, '.openclaw/workspace/trading');
const TRAIL_STATE_FILE = path.join(TRADING_DIR, 'trailing_tp_state.json');

// Configuration
const TRAIL_PERCENT = 0.01; // 1% trail distance
const MIN_PROFIT_PERCENT = 0.005; // Minimum 0.5% profit before trailing activates

class TrailingTPManager {
  constructor() {
    this.loadState();
  }

  loadState() {
    if (fs.existsSync(TRAIL_STATE_FILE)) {
      this.state = JSON.parse(fs.readFileSync(TRAIL_STATE_FILE, 'utf-8'));
    } else {
      this.state = {
        positions: {}, // symbol -> { bestPrice, trailTP, activated }
        history: []
      };
    }
  }

  saveState() {
    fs.writeFileSync(TRAIL_STATE_FILE, JSON.stringify(this.state, null, 2));
  }

  getCurrentPrice(symbol) {
    try {
      const result = execSync(`python3 binance_api.py price ${symbol}`, {
        encoding: 'utf-8',
        cwd: TRADING_DIR,
        timeout: 5000
      });
      return JSON.parse(result.trim()).price;
    } catch (e) {
      return null;
    }
  }

  getPositions() {
    try {
      const result = execSync('python3 binance_api.py positions', {
        encoding: 'utf-8',
        cwd: TRADING_DIR,
        timeout: 10000
      });
      return JSON.parse(result.trim());
    } catch (e) {
      return [];
    }
  }

  closePosition(symbol) {
    try {
      // Close position via Binance testnet API
      console.log(`🚨 TRAILING TP TRIGGERED: Closing ${symbol}`);
      const result = execSync(`python3 binance_api.py close ${symbol}`, {
        encoding: 'utf-8',
        cwd: TRADING_DIR,
        timeout: 10000
      });
      console.log('Close result:', result);
      return true;
    } catch (e) {
      console.error(`Error closing ${symbol}:`, e.message);
      return false;
    }
  }

  update() {
    console.log('\n' + '='.repeat(70));
    console.log('📈 TRAILING TAKE PROFIT MONITOR');
    console.log(`⏰ ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}`);
    console.log('='.repeat(70));

    const positions = this.getPositions();
    if (!positions || positions.length === 0) {
      console.log('No open positions.');
      return;
    }

    let actions = [];

    for (const pos of positions) {
      const symbol = pos.symbol;
      const side = pos.side;
      const entryPrice = pos.entry_price;
      const currentPrice = this.getCurrentPrice(symbol);

      if (!currentPrice) {
        console.log(`⚠️ ${symbol}: Could not fetch price`);
        continue;
      }

      // Calculate current profit
      let profitPercent = 0;
      if (side === 'SHORT') {
        profitPercent = (entryPrice - currentPrice) / entryPrice;
      } else {
        profitPercent = (currentPrice - entryPrice) / entryPrice;
      }

      // Initialize state if not exists
      if (!this.state.positions[symbol]) {
        this.state.positions[symbol] = {
          entryPrice,
          side,
          bestPrice: currentPrice,
          trailTP: null,
          activated: false,
          startTime: new Date().toISOString()
        };
      }

      const state = this.state.positions[symbol];

      // Check if trailing should activate (minimum profit reached)
      if (!state.activated && profitPercent >= MIN_PROFIT_PERCENT) {
        state.activated = true;
        state.bestPrice = currentPrice;
        // Set initial trail TP
        if (side === 'SHORT') {
          state.trailTP = currentPrice * (1 + TRAIL_PERCENT);
        } else {
          state.trailTP = currentPrice * (1 - TRAIL_PERCENT);
        }
        console.log(`🎯 ${symbol}: Trailing TP ACTIVATED at ${state.trailTP.toFixed(4)}`);
      }

      // If activated, check for price improvement or reversal
      if (state.activated) {
        if (side === 'SHORT') {
          // For SHORT: price going DOWN is good
          if (currentPrice < state.bestPrice) {
            // Price improved - update trail
            state.bestPrice = currentPrice;
            state.trailTP = currentPrice * (1 + TRAIL_PERCENT);
            console.log(`📉 ${symbol}: Trail updated to ${state.trailTP.toFixed(4)} (price: ${currentPrice.toFixed(4)})`);
          }
          // Check if price reversed above trail TP
          if (currentPrice >= state.trailTP) {
            console.log(`🚨 ${symbol}: TRAILING TP HIT at ${currentPrice.toFixed(4)}`);
            actions.push({ symbol, reason: 'TRAILING_TP', price: currentPrice });
          }
        } else {
          // For LONG: price going UP is good
          if (currentPrice > state.bestPrice) {
            state.bestPrice = currentPrice;
            state.trailTP = currentPrice * (1 - TRAIL_PERCENT);
            console.log(`📈 ${symbol}: Trail updated to ${state.trailTP.toFixed(4)} (price: ${currentPrice.toFixed(4)})`);
          }
          if (currentPrice <= state.trailTP) {
            console.log(`🚨 ${symbol}: TRAILING TP HIT at ${currentPrice.toFixed(4)}`);
            actions.push({ symbol, reason: 'TRAILING_TP', price: currentPrice });
          }
        }
      }

      // Print status
      const pnl = (profitPercent * 100).toFixed(2);
      const status = profitPercent >= 0 ? '✅' : '❌';
      console.log(`${status} ${symbol}: Entry $${entryPrice.toFixed(4)} → Current $${currentPrice.toFixed(4)} | PnL: ${pnl}% | Trail TP: ${state.trailTP ? '$' + state.trailTP.toFixed(4) : 'Not activated'}`);
    }

    // Execute close actions
    for (const action of actions) {
      const closed = this.closePosition(action.symbol);
      if (closed) {
        delete this.state.positions[action.symbol];
        this.state.history.push({
          symbol: action.symbol,
          reason: action.reason,
          price: action.price,
          time: new Date().toISOString()
        });
      }
    }

    this.saveState();

    console.log('\n' + '='.repeat(70));
    console.log(`📊 Trailing TP Status: ${Object.keys(this.state.positions).length} positions tracked`);
    console.log('='.repeat(70));
  }
}

// Run if called directly
if (require.main === module) {
  const manager = new TrailingTPManager();
  manager.update();
}

module.exports = TrailingTPManager;

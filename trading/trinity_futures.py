#!/usr/bin/env python3
"""
TRINITY FUTURES ORCHESTRATOR

Complete futures trading system with:
- Multi-agent ensemble (4 AI models)
- Binance Futures integration (HMAC auth)
- Paper trading with full logging
- Dashboard for trade decisions

Usage:
    python trinity_futures.py scan           # Scan market
    python trinity_futures.py analyze BTC    # Analyze specific pair
    python trinity_futures.py dashboard      # Open dashboard
    python trinity_futures.py performance    # Show performance
"""

import os
import sys
import json
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional

# Load environment
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from radar_agent import RadarAgent
from scanner import MarketScanner
from ensemble_engine import EnsembleEngine, Signal
from binance_futures import BinanceFuturesExecutor


class TrinityFutures:
    """
    Complete futures trading orchestrator.
    
    Integrates:
    - Radar Agent (data verification)
    - Market Scanner (confluence scoring)
    - Ensemble Engine (multi-model consensus)
    - Binance Futures Executor (paper trading)
    """
    
    # Futures pairs
    FUTURES_PAIRS = [
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
        'DOGEUSDT', 'ADAUSDT', 'AVAXUSDT', 'DOTUSDT', 'MATICUSDT',
        'LINKUSDT', 'UNIUSDT', 'ATOMUSDT', 'LTCUSDT', 'ETCUSDT'
    ]
    
    def __init__(self, 
                 testnet: bool = True,
                 initial_capital: float = 10000,
                 max_leverage: int = 5):
        """Initialize Trinity Futures system."""
        self.testnet = testnet
        self.max_leverage = max_leverage
        
        # Initialize components
        self.radar = RadarAgent(testnet=testnet)
        self.scanner = MarketScanner(testnet=testnet)
        self.ensemble = EnsembleEngine(consensus_threshold=0.75)
        self.executor = BinanceFuturesExecutor(
            testnet=testnet,
            max_leverage=max_leverage
        )
        
        self.results = {
            'timestamp': None,
            'scans': [],
            'signals': [],
            'trades': []
        }
    
    def analyze_pair(self, symbol: str, timeframe: str = '4h') -> Dict:
        """
        Full analysis pipeline for a single pair.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            timeframe: Chart interval
            
        Returns:
            Complete analysis result
        """
        # Convert to CCXT format if needed
        ccxt_symbol = symbol.replace('USDT', '/USDT')
        
        print(f"\n{'='*70}")
        print(f"TRINITY FUTURES ANALYSIS: {symbol}")
        print(f"{'='*70}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Radar verification
        print(f"\n📡 Step 1: RADAR - Data Verification")
        regime = self.radar.get_market_regime(ccxt_symbol, timeframe)
        
        if 'error' in regime:
            return {'error': regime['error'], 'symbol': symbol}
        
        print(f"   Regime: {regime.get('regime', 'N/A')}")
        print(f"   Trade Allowed: {regime.get('trade_allowed', False)}")
        
        # Step 2: Scanner confluence
        print(f"\n📊 Step 2: SCANNER - Confluence Analysis")
        scan_result = self.scanner.scan_pair(ccxt_symbol, timeframe)
        confluence = scan_result.get('confluence_score', 0)
        
        print(f"   Confluence Score: {confluence}%")
        print(f"   Status: {scan_result.get('status', 'N/A')}")
        
        # Step 3: Ensemble consensus
        print(f"\n🤖 Step 3: ENSEMBLE - Multi-Model Consensus")
        
        market_data = {
            'symbol': symbol,
            'price': regime.get('real_data', {}).get('price', 0),
            'rsi': regime.get('real_data', {}).get('rsi', 50),
            'macd': regime.get('real_data', {}).get('macd', {}),
            'adx': regime.get('adx', {}),
            'bollinger': regime.get('bollinger', {}),
            'tbo': regime.get('tbo', {}),
            'regime': regime.get('regime', 'unknown'),
            'trade_allowed': regime.get('trade_allowed', False)
        }
        
        ensemble_result = self.ensemble.run_ensemble(ccxt_symbol, market_data, simulate=True)
        
        # Step 4: Decision
        print(f"\n{'='*70}")
        print("TRINITY DECISION")
        print(f"{'='*70}")
        
        should_trade = (
            regime.get('trade_allowed', False) and
            confluence >= 70 and
            ensemble_result.should_trade
        )
        
        result = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'radar': regime,
            'scanner': scan_result,
            'ensemble': ensemble_result,
            'should_trade': should_trade
        }
        
        print(f"Action: {ensemble_result.signal.value}")
        print(f"Should Trade: {'✅ YES' if should_trade else '❌ NO'}")
        
        # Step 5: Execute if conditions met
        if should_trade and ensemble_result.signal.value in ['LONG', 'SHORT']:
            print(f"\n💰 EXECUTING FUTURES TRADE...")
            self._execute_futures_trade(symbol, ensemble_result, scan_result, regime)
        
        return result
    
    def _execute_futures_trade(self, 
                               symbol: str,
                               ensemble_result,
                               scan_result: Dict,
                               regime: Dict) -> Optional[Dict]:
        """Execute a futures trade."""
        # Get current price
        current_price = self.executor.get_current_price(symbol)
        if current_price == 0:
            print(f"❌ Failed to get price for {symbol}")
            return None
        
        # Determine side
        side = 'BUY' if ensemble_result.signal.value == 'LONG' else 'SELL'
        
        # Calculate position size (5% of balance)
        balance = self.executor.get_balance()
        position_size_usd = balance * 0.05
        quantity = position_size_usd / current_price
        
        # Round quantity to proper precision
        quantity = round(quantity, 3)
        
        # Calculate SL/TP (2% SL, 4% TP)
        if side == 'BUY':
            stop_loss = current_price * 0.98
            take_profit = current_price * 1.04
        else:
            stop_loss = current_price * 1.02
            take_profit = current_price * 0.96
        
        # Set leverage (use lower for paper trading)
        leverage = min(3, self.max_leverage)
        
        # Execute trade
        print(f"   Symbol: {symbol}")
        print(f"   Side: {side} ({ensemble_result.signal.value})")
        print(f"   Price: ${current_price:,.2f}")
        print(f"   Quantity: {quantity}")
        print(f"   Leverage: {leverage}x")
        print(f"   Stop Loss: ${stop_loss:,.2f}")
        print(f"   Take Profit: ${take_profit:,.2f}")
        
        result = self.executor.open_position(
            symbol=symbol,
            side=side,
            quantity=quantity,
            leverage=leverage,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        
        if 'error' in result:
            print(f"❌ Trade failed: {result['error']}")
            return None
        
        print(f"✅ Trade executed: {result.get('orderId', 'N/A')}")
        
        return result
    
    def scan_market(self, pairs: List[str] = None) -> List[Dict]:
        """Scan multiple pairs."""
        if pairs is None:
            pairs = self.FUTURES_PAIRS[:5]  # Top 5 for speed
        
        results = []
        
        print(f"\n{'='*70}")
        print("TRINITY FUTURES SCAN")
        print(f"{'='*70}")
        print(f"Scanning {len(pairs)} pairs")
        print(f"{'='*70}\n")
        
        for i, symbol in enumerate(pairs, 1):
            print(f"\n[{i}/{len(pairs)}] {symbol}")
            result = self.analyze_pair(symbol)
            results.append(result)
        
        # Find signals
        signals = [r for r in results if r.get('should_trade', False)]
        
        print(f"\n{'='*70}")
        print("SCAN SUMMARY")
        print(f"{'='*70}")
        print(f"Total scanned: {len(results)}")
        print(f"Signals found: {len(signals)}")
        
        if signals:
            print(f"\n🚨 ACTIVE SIGNALS:")
            for s in signals:
                ens = s.get('ensemble')
                if ens:
                    print(f"   {s['symbol']}: {ens.signal.value}")
        
        return results
    
    def show_positions(self):
        """Show current positions."""
        positions = self.executor.get_positions()
        
        print(f"\n{'='*70}")
        print("OPEN POSITIONS")
        print(f"{'='*70}")
        
        if not positions:
            print("No open positions")
        else:
            for pos in positions:
                pnl_str = f"${pos['unrealized_pnl']:+,.2f}"
                print(f"{pos['symbol']}: {pos['side']} {abs(pos['size'])} @ ${pos['entry_price']:,.2f} | P&L: {pnl_str}")
    
    def show_performance(self):
        """Show performance summary."""
        balance = self.executor.get_balance()
        positions = self.executor.get_positions()
        
        print(f"\n{'='*70}")
        print("📊 PERFORMANCE SUMMARY")
        print(f"{'='*70}")
        print(f"Balance: ${balance:,.2f} USDT")
        print(f"Open Positions: {len(positions)}")
        print(f"Circuit Breaker: {'ACTIVE 🚨' if self.executor.circuit_breaker_active else 'Inactive'}")
        print(f"{'='*70}\n")
    
    def open_dashboard(self):
        """Open trading dashboard in browser."""
        dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.html')
        webbrowser.open(f'file://{dashboard_path}')
        print(f"✅ Dashboard opened in browser")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python trinity_futures.py [scan|analyze|positions|performance|dashboard] [symbol]")
        return
    
    command = sys.argv[1].lower()
    
    # Initialize system
    trinity = TrinityFutures(testnet=True, max_leverage=5)
    
    if command == 'scan':
        pairs = sys.argv[2:] if len(sys.argv) > 2 else None
        trinity.scan_market(pairs)
    
    elif command == 'analyze':
        symbol = sys.argv[2] if len(sys.argv) > 2 else 'BTCUSDT'
        trinity.analyze_pair(symbol)
    
    elif command == 'positions':
        trinity.show_positions()
    
    elif command == 'performance':
        trinity.show_performance()
    
    elif command == 'dashboard':
        trinity.open_dashboard()
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()

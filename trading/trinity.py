#!/usr/bin/env python3
"""
TRINITY TRADING ORCHESTRATOR

Main entry point for the Trinity Trading System.
Coordinates Radar, Scanner, Ensemble, and Executor.

Usage:
    python trinity.py scan          # Run market scan
    python trinity.py ensemble      # Run ensemble analysis
    python trinity.py analyze BTC   # Deep analysis of specific pair
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

# Import components
from radar_agent import RadarAgent
from scanner import MarketScanner
from ensemble_engine import EnsembleEngine, Signal
from executor import PaperTradeExecutor


class TrinityOrchestrator:
    """
    Main orchestrator for the Trinity Trading System.
    
    Coordinates all components:
    - Radar Agent: Data verification
    - Market Scanner: Signal generation
    - Ensemble Engine: Multi-model consensus
    - Executor: Paper trade execution (TODO)
    """
    
    def __init__(self, testnet: bool = True, initial_capital: float = 10000.0):
        """Initialize Trinity system."""
        self.radar = RadarAgent(testnet=testnet)
        self.scanner = MarketScanner(testnet=testnet)
        self.ensemble = EnsembleEngine(consensus_threshold=0.75)
        self.executor = PaperTradeExecutor(initial_capital=initial_capital)
        
        self.results = {
            'timestamp': None,
            'scans': [],
            'ensemble_results': [],
            'signals': [],
            'trades': []
        }
    
    def run_full_analysis(self, symbol: str, timeframe: str = '4h') -> Dict:
        """
        Run full analysis pipeline on a symbol.
        
        1. Radar fetches and verifies data
        2. Scanner calculates confluence
        3. Ensemble gets multi-model consensus
        4. Returns combined result
        
        Args:
            symbol: Trading pair
            timeframe: Chart interval
            
        Returns:
            Complete analysis result
        """
        print(f"\n{'='*70}")
        print(f"TRINITY ANALYSIS: {symbol}")
        print(f"{'='*70}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Timeframe: {timeframe}")
        print(f"{'='*70}\n")
        
        # Step 1: Radar verification
        print("📡 Step 1: RADAR - Data Verification")
        print("-" * 50)
        regime = self.radar.get_market_regime(symbol, timeframe)
        
        if 'error' in regime:
            return {'error': regime['error'], 'symbol': symbol}
        
        print(f"   Regime: {regime.get('regime', 'N/A')}")
        print(f"   Trade Allowed: {regime.get('trade_allowed', False)}")
        
        # Step 2: Scanner confluence
        print(f"\n📊 Step 2: SCANNER - Confluence Analysis")
        print("-" * 50)
        scan_result = self.scanner.scan_pair(symbol, timeframe)
        confluence = scan_result.get('confluence_score', 0)
        
        print(f"   Confluence Score: {confluence}%")
        print(f"   Status: {scan_result.get('status', 'N/A')}")
        
        # Step 3: Ensemble consensus
        print(f"\n🤖 Step 3: ENSEMBLE - Multi-Model Consensus")
        print("-" * 50)
        
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
        
        ensemble_result = self.ensemble.run_ensemble(symbol, market_data, simulate=True)
        
        # Step 4: Combine results
        print(f"\n{'='*70}")
        print("TRINITY DECISION")
        print(f"{'='*70}")
        
        should_trade = (
            regime.get('trade_allowed', False) and
            confluence >= 70 and
            ensemble_result.should_trade
        )
        
        final_signal = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'radar': {
                'verified': True,
                'regime': regime.get('regime'),
                'trade_allowed': regime.get('trade_allowed')
            },
            'scanner': {
                'confluence_score': confluence,
                'status': scan_result.get('status')
            },
            'ensemble': {
                'signal': ensemble_result.signal.value,
                'agreement': f"{ensemble_result.agreement_ratio*100:.0f}%",
                'confidence': f"{ensemble_result.confidence:.1f}%",
                'should_trade': ensemble_result.should_trade
            },
            'final_decision': {
                'action': ensemble_result.signal.value if should_trade else 'WAIT',
                'should_trade': should_trade,
                'confidence': confluence if should_trade else 0
            }
        }
        
        # Step 5: Execute trade if conditions met
        trade = None
        if should_trade and ensemble_result.signal.value in ['LONG', 'SHORT']:
            print(f"\n💰 EXECUTING PAPER TRADE...")
            trade = self.executor.execute_trade(
                symbol=symbol,
                action=ensemble_result.signal.value,
                entry_price=regime.get('real_data', {}).get('price', 0),
                ensemble_result=ensemble_result,
                scan_result=scan_result,
                regime_data=regime
            )
            if trade:
                final_signal['trade'] = {
                    'trade_id': trade.trade_id,
                    'status': 'OPENED',
                    'position_size': trade.position_size
                }
        
        print(f"Action: {final_signal['final_decision']['action']}")
        print(f"Should Trade: {'✅ YES' if should_trade else '❌ NO'}")
        print(f"Confidence: {final_signal['final_decision']['confidence']}%")
        
        print(f"\n{'='*70}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*70}\n")
        
        return final_signal
    
    def scan_market(self, pairs: List[str] = None, timeframe: str = '4h') -> List[Dict]:
        """
        Scan multiple pairs with full analysis.
        
        Args:
            pairs: List of trading pairs
            timeframe: Chart interval
            
        Returns:
            List of analysis results
        """
        if pairs is None:
            pairs = self.scanner.DEFAULT_PAIRS[:10]  # Top 10 for speed
        
        results = []
        
        print(f"\n{'='*70}")
        print("TRINITY MARKET SCAN")
        print(f"{'='*70}")
        print(f"Scanning {len(pairs)} pairs on {timeframe}")
        print(f"{'='*70}\n")
        
        for i, symbol in enumerate(pairs, 1):
            print(f"\n[{i}/{len(pairs)}] {symbol}")
            result = self.run_full_analysis(symbol, timeframe)
            results.append(result)
        
        # Find signals
        signals = [r for r in results if r.get('final_decision', {}).get('should_trade', False)]
        
        print(f"\n{'='*70}")
        print("SCAN SUMMARY")
        print(f"{'='*70}")
        print(f"Total scanned: {len(results)}")
        print(f"Signals found: {len(signals)}")
        
        if signals:
            print(f"\n🚨 ACTIVE SIGNALS:")
            for s in signals:
                fd = s.get('final_decision', {})
                print(f"   {s['symbol']}: {fd.get('action')} ({fd.get('confidence')}% confidence)")
        
        self.results['timestamp'] = datetime.now().isoformat()
        self.results['signals'] = signals
        
        return results
    
    def show_performance(self):
        """Show trading performance summary."""
        self.executor.print_summary()
    
    def close_all_trades(self, exit_prices: Dict[str, float]):
        """
        Close all open trades.
        
        Args:
            exit_prices: Dict mapping symbol to exit price
        """
        open_trades = [t for t in self.executor.trades if t.status == "OPEN"]
        
        for trade in open_trades:
            exit_price = exit_prices.get(trade.symbol)
            if exit_price:
                self.executor.close_trade(
                    trade.trade_id, 
                    exit_price, 
                    reason="End of session"
                )
        
        self.show_performance()
    
    def save_results(self, filepath: str = None):
        """Save results to JSON."""
        if filepath is None:
            filepath = f"trinity_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = f"/Users/michaelnetto/.openclaw/workspace/trading/{filepath}"
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n📁 Results saved to {filepath}")


def main():
    """Main entry point."""
    trinity = TrinityOrchestrator(testnet=True)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'scan':
            pairs = sys.argv[2:] if len(sys.argv) > 2 else None
            trinity.scan_market(pairs)
            trinity.show_performance()
        
        elif command == 'analyze':
            symbol = sys.argv[2] if len(sys.argv) > 2 else 'BTC/USDT'
            trinity.run_full_analysis(symbol)
        
        elif command == 'performance':
            trinity.show_performance()
        
        else:
            print(f"Unknown command: {command}")
            print("Usage: python trinity.py [scan|analyze|performance] [symbol]")
    else:
        # Default: analyze BTC
        trinity.run_full_analysis('BTC/USDT')
    
    trinity.save_results()


if __name__ == '__main__':
    main()

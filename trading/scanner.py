#!/usr/bin/env python3
"""
MARKET SCANNER - Multi-Agent Trading Scanner

Scans cryptocurrency markets for trading opportunities using:
- Radar agent for data verification (anti-hallucination)
- TBO-style signals for trend detection
- ADX + Bollinger for regime filtering
- Cycle degradation awareness (new listings focus)

Based on research from:
- Michael Automates: Backtesting, strategy comparison
- Aaron Dishner: TBO indicator, new listings advantage
- Across the Rubicon: Multi-agent architecture, circuit breakers
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from radar_agent import RadarAgent
from datetime import datetime
from typing import Dict, List, Optional
import json


class MarketScanner:
    """
    Multi-agent market scanner for cryptocurrency trading.
    
    Combines:
    - Radar agent (data verification)
    - TBO signals (trend detection)
    - ADX regime filter (trend strength)
    - Bollinger volatility filter
    - Confluence scoring (0-100)
    """
    
    # Top trading pairs by volume
    DEFAULT_PAIRS = [
        'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT',
        'DOGE/USDT', 'ADA/USDT', 'AVAX/USDT', 'DOT/USDT', 'MATIC/USDT',
        'LINK/USDT', 'UNI/USDT', 'ATOM/USDT', 'LTC/USDT', 'ETC/USDT',
        'NEAR/USDT', 'APT/USDT', 'AR/USDT', 'OP/USDT', 'ARB/USDT'
    ]
    
    def __init__(self, testnet: bool = True):
        """
        Initialize market scanner.
        
        Args:
            testnet: Use testnet/demo mode (default: True for safety)
        """
        self.radar = RadarAgent(testnet=testnet)
        self.scan_results = []
        self.confluence_threshold = 70  # Minimum score to generate signal
    
    def calculate_confluence_score(self, regime: Dict) -> int:
        """
        Calculate confluence score (0-100) for trading signal.
        
        Higher score = more confluence = higher confidence
        
        Components:
        - TBO signal (30 pts)
        - RSI favorable (20 pts)
        - ADX trend strength (20 pts)
        - Volume spike (15 pts)
        - Bollinger position (15 pts)
        
        Args:
            regime: Market regime data from Radar
            
        Returns:
            Confluence score (0-100)
        """
        score = 0
        breakdown = {}
        
        # TBO Signal (30 pts)
        tbo = regime.get('tbo', {})
        if tbo.get('signal') == 'bullish':
            score += 15
            breakdown['tbo_signal'] = 15
        elif tbo.get('signal') == 'bearish':
            score += 10  # Less for bearish (long-bias from Michael)
            breakdown['tbo_signal'] = 10
        
        if tbo.get('crossover') == 'bullish_cross':
            score += 15
            breakdown['tbo_crossover'] = 15
        elif tbo.get('crossover') == 'bearish_cross':
            score += 10
            breakdown['tbo_crossover'] = 10
        
        # RSI favorable (20 pts)
        rsi = regime.get('real_data', {}).get('rsi', 50) if 'real_data' in regime else 50
        if rsi < 30:  # Oversold - bullish
            score += 20
            breakdown['rsi'] = 20
        elif rsi < 40:
            score += 15
            breakdown['rsi'] = 15
        elif rsi > 70:  # Overbought - bearish
            score += 5
            breakdown['rsi'] = 5
        elif 40 < rsi < 60:  # Neutral - good for trending
            score += 10
            breakdown['rsi'] = 10
        
        # ADX trend strength (20 pts)
        adx = regime.get('adx', {})
        if adx.get('adx', 0) > 25:
            score += 15
            breakdown['adx'] = 15
        if adx.get('adx', 0) > 35:
            score += 5  # Bonus for strong trend
            breakdown['adx_bonus'] = 5
        
        # Bollinger position (15 pts)
        bollinger = regime.get('bollinger', {})
        if bollinger.get('position') == 'below':
            score += 15  # Near lower band = potential bounce
            breakdown['bollinger'] = 15
        elif bollinger.get('position') == 'inside':
            score += 5
            breakdown['bollinger'] = 5
        
        # Regime check (bonus/penalty)
        if regime.get('regime') == 'trending':
            score += 0  # No change, good for trend following
        elif regime.get('regime') == 'ranging':
            score -= 10  # Penalty for choppy market
            breakdown['regime_penalty'] = -10
        elif regime.get('regime') == 'volatile':
            score -= 5
            breakdown['regime_penalty'] = -5
        
        return min(100, max(0, score)), breakdown
    
    def scan_pair(self, symbol: str, timeframe: str = '4h') -> Dict:
        """
        Scan a single trading pair for signals.
        
        Args:
            symbol: Trading pair
            timeframe: Chart timeframe
            
        Returns:
            Scan result with confluence score and recommendation
        """
        result = {
            'symbol': symbol,
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'status': 'NO_SIGNAL',
            'confluence_score': 0,
            'recommendation': None
        }
        
        # Get market regime from Radar
        regime = self.radar.get_market_regime(symbol, timeframe)
        
        if 'error' in regime:
            result['error'] = regime['error']
            return result
        
        result['regime'] = regime
        
        # Check if trading allowed
        if not regime.get('trade_allowed', False):
            result['status'] = 'FILTERED'
            result['reason'] = regime.get('reason', ['Unknown'])
            return result
        
        # Calculate confluence score
        score, breakdown = self.calculate_confluence_score(regime)
        result['confluence_score'] = score
        result['confluence_breakdown'] = breakdown
        
        # Determine signal
        if score >= self.confluence_threshold:
            tbo_signal = regime.get('tbo', {}).get('signal', 'neutral')
            
            if tbo_signal == 'bullish':
                result['status'] = 'LONG_SIGNAL'
                result['recommendation'] = {
                    'action': 'LONG',
                    'entry': regime.get('real_data', {}).get('price', 0),
                    'stop_loss': regime.get('bollinger', {}).get('lower', 0),
                    'take_profit': regime.get('bollinger', {}).get('upper', 0),
                    'confidence': f"{score}%"
                }
            elif tbo_signal == 'bearish':
                result['status'] = 'SHORT_SIGNAL'
                result['recommendation'] = {
                    'action': 'SHORT',
                    'entry': regime.get('real_data', {}).get('price', 0),
                    'stop_loss': regime.get('bollinger', {}).get('upper', 0),
                    'take_profit': regime.get('bollinger', {}).get('lower', 0),
                    'confidence': f"{score}%"
                }
        else:
            result['status'] = 'NO_SIGNAL'
            result['reason'] = f"Score {score} below threshold {self.confluence_threshold}"
        
        return result
    
    def scan_market(self, pairs: List[str] = None, timeframe: str = '4h') -> List[Dict]:
        """
        Scan multiple trading pairs for signals.
        
        Args:
            pairs: List of trading pairs (default: top 20 by volume)
            timeframe: Chart timeframe
            
        Returns:
            List of scan results
        """
        if pairs is None:
            pairs = self.DEFAULT_PAIRS
        
        results = []
        signals = []
        
        print(f"\n{'=' * 60}")
        print(f"MARKET SCAN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 60}")
        print(f"Scanning {len(pairs)} pairs on {timeframe} timeframe...")
        print(f"Confluence threshold: {self.confluence_threshold}%")
        print(f"{'=' * 60}\n")
        
        for i, symbol in enumerate(pairs, 1):
            print(f"[{i}/{len(pairs)}] Scanning {symbol}...", end=" ")
            
            result = self.scan_pair(symbol, timeframe)
            results.append(result)
            
            status = result.get('status', 'UNKNOWN')
            score = result.get('confluence_score', 0)
            
            if status in ['LONG_SIGNAL', 'SHORT_SIGNAL']:
                print(f"✅ {status} (Score: {score}%)")
                signals.append(result)
            elif status == 'FILTERED':
                print(f"🚫 FILTERED")
            else:
                print(f"➖ {status} (Score: {score}%)")
        
        self.scan_results = results
        
        # Summary
        print(f"\n{'=' * 60}")
        print("SCAN SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total scanned: {len(results)}")
        print(f"Signals found: {len(signals)}")
        
        if signals:
            print(f"\n🚨 SIGNALS:")
            for s in signals:
                rec = s.get('recommendation', {})
                print(f"   {s['symbol']}: {rec.get('action', 'N/A')} @ ${rec.get('entry', 0):,.2f}")
                print(f"      Confidence: {rec.get('confidence', 'N/A')}")
        else:
            print(f"\n✋ No signals above threshold")
        
        return results
    
    def get_top_signals(self, limit: int = 5) -> List[Dict]:
        """
        Get top signals sorted by confluence score.
        
        Args:
            limit: Maximum number of signals to return
            
        Returns:
            List of top signals
        """
        signals = [r for r in self.scan_results if r.get('status') in ['LONG_SIGNAL', 'SHORT_SIGNAL']]
        signals.sort(key=lambda x: x.get('confluence_score', 0), reverse=True)
        return signals[:limit]
    
    def save_results(self, filepath: str = None):
        """
        Save scan results to JSON file.
        
        Args:
            filepath: Output file path
        """
        if filepath is None:
            filepath = os.path.join(os.path.dirname(__file__), 'scan_results.json')
        
        with open(filepath, 'w') as f:
            json.dump(self.scan_results, f, indent=2, default=str)
        
        print(f"Results saved to {filepath}")


def main():
    """Run market scanner."""
    scanner = MarketScanner(testnet=True)
    
    # Scan top pairs
    results = scanner.scan_market(timeframe='4h')
    
    # Save results
    scanner.save_results()
    
    # Print top signals
    top_signals = scanner.get_top_signals()
    
    if top_signals:
        print(f"\n🎯 TOP SIGNALS:")
        for i, signal in enumerate(top_signals, 1):
            print(f"\n{i}. {signal['symbol']}")
            print(f"   Status: {signal['status']}")
            print(f"   Score: {signal['confluence_score']}%")
            print(f"   Breakdown: {signal.get('confluence_breakdown', {})}")
            rec = signal.get('recommendation', {})
            if rec:
                print(f"   Entry: ${rec.get('entry', 0):,.2f}")
                print(f"   Stop Loss: ${rec.get('stop_loss', 0):,.2f}")
                print(f"   Take Profit: ${rec.get('take_profit', 0):,.2f}")
    else:
        print("\n✋ No signals found above threshold")
    
    print("\n" + "=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()

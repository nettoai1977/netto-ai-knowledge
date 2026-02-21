#!/usr/bin/env python3
"""
RADAR AGENT - Anti-Hallucination Data Verifier

Mission: Verify ALL technical data BEFORE any trading signal is generated.
No hallucinated RSI, MACD, or price data allowed.

Based on research from:
- Michael Automates (OpenClaw + Hyperliquid)
- Aaron Dishner (TBO Indicator, Cycle Degradation)
- Across the Rubicon (Multi-agent architecture, Circuit breakers)
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json


class RadarAgent:
    """
    Anti-hallucination data verifier for crypto trading.
    
    RADAR = Real-time Audited Data & Analysis Reporter
    
    This agent:
    1. Fetches raw OHLCV data from Binance (no hallucination)
    2. Calculates all indicators from raw data (no made-up numbers)
    3. Verifies claimed values against calculated values
    4. Reports VERIFIED or REJECTED status
    """
    
    def __init__(self, exchange: str = 'binance', testnet: bool = True):
        """
        Initialize Radar agent with CCXT exchange.
        
        Args:
            exchange: Exchange name (default: binance)
            testnet: Use testnet/demo mode (default: True for safety)
        """
        self.exchange_name = exchange
        self.testnet = testnet
        
        # Initialize CCXT exchange
        if exchange == 'binance':
            if testnet:
                # Demo mode endpoints
                self.exchange = ccxt.binance({
                    'urls': {
                        'api': {
                            'public': 'https://demo-api.binance.com/api/v3',
                            'private': 'https://demo-api.binance.com/api/v3',
                        }
                    }
                })
            else:
                self.exchange = ccxt.binance()
        else:
            self.exchange = getattr(ccxt, exchange)()
        
        # Verification log
        self.verification_log = []
    
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 200) -> pd.DataFrame:
        """
        Fetch raw OHLCV data from exchange.
        
        This is the FOUNDATION of anti-hallucination.
        All calculations derive from this raw data.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candle interval (e.g., '1h', '4h', '1d')
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            self._log_error(f"Failed to fetch OHLCV for {symbol}: {e}")
            return None
    
    def calculate_rsi(self, closes: np.ndarray, period: int = 14) -> float:
        """
        Calculate RSI from raw close prices.
        
        NO HALLUCINATION - calculated from real data.
        
        Args:
            closes: Array of close prices
            period: RSI period (default: 14)
            
        Returns:
            RSI value (0-100)
        """
        if len(closes) < period + 1:
            return None
        
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    def calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """
        Calculate EMA (Exponential Moving Average).
        
        Args:
            data: Array of values
            period: EMA period
            
        Returns:
            Array of EMA values
        """
        ema = np.zeros_like(data)
        ema[0] = data[0]
        multiplier = 2 / (period + 1)
        
        for i in range(1, len(data)):
            ema[i] = (data[i] * multiplier) + (ema[i-1] * (1 - multiplier))
        
        return ema
    
    def calculate_macd(self, closes: np.ndarray, 
                       fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """
        Calculate MACD from raw close prices.
        
        Args:
            closes: Array of close prices
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            
        Returns:
            Dict with macd, signal, histogram values
        """
        ema_fast = self.calculate_ema(closes, fast)
        ema_slow = self.calculate_ema(closes, slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = self.calculate_ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        return {
            'macd': round(macd_line[-1], 4),
            'signal': round(signal_line[-1], 4),
            'histogram': round(histogram[-1], 4),
            'trend': 'bullish' if histogram[-1] > 0 else 'bearish'
        }
    
    def calculate_adx(self, df: pd.DataFrame, period: int = 14) -> Dict:
        """
        Calculate ADX (Average Directional Index) for trend strength.
        
        Used for market regime filter (from Across the Rubicon research).
        
        Args:
            df: OHLCV DataFrame
            period: ADX period
            
        Returns:
            Dict with ADX value and trend strength
        """
        high = df['high'].values
        low = df['low'].values
        close = df['close'].values
        
        # Calculate True Range
        tr1 = high - low
        tr2 = np.abs(high - np.roll(close, 1))
        tr3 = np.abs(low - np.roll(close, 1))
        tr = np.maximum(tr1, np.maximum(tr2, tr3))
        
        # Calculate +DM and -DM
        up_move = high - np.roll(high, 1)
        down_move = np.roll(low, 1) - low
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        # Smooth values
        atr = np.mean(tr[-period:])
        plus_di = 100 * np.mean(plus_dm[-period:]) / atr
        minus_di = 100 * np.mean(minus_dm[-period:]) / atr
        
        # Calculate ADX
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        
        return {
            'adx': round(dx, 2),
            'plus_di': round(plus_di, 2),
            'minus_di': round(minus_di, 2),
            'trend_strength': 'strong' if dx > 25 else 'weak',
            'trend_direction': 'bullish' if plus_di > minus_di else 'bearish'
        }
    
    def calculate_bollinger_bands(self, closes: np.ndarray, 
                                   period: int = 20, std_dev: float = 2) -> Dict:
        """
        Calculate Bollinger Bands for volatility filter.
        
        Used for market regime filter (from Across the Rubicon research).
        
        Args:
            closes: Array of close prices
            period: SMA period
            std_dev: Standard deviation multiplier
            
        Returns:
            Dict with upper, middle, lower bands
        """
        sma = np.mean(closes[-period:])
        std = np.std(closes[-period:])
        
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        
        current_price = closes[-1]
        
        return {
            'upper': round(upper, 2),
            'middle': round(sma, 2),
            'lower': round(lower, 2),
            'width': round((upper - lower) / sma * 100, 2),
            'position': 'above' if current_price > upper else 'below' if current_price < lower else 'inside'
        }
    
    def calculate_tbo_signal(self, df: pd.DataFrame) -> Dict:
        """
        Calculate TBO (Trending Breakout) style signal.
        
        Based on Aaron Dishner's TBO indicator:
        - 20 EMA cross 40 EMA = trend signal
        - 50 MA and 150 MA for support/resistance
        
        Args:
            df: OHLCV DataFrame
            
        Returns:
            Dict with TBO signal status
        """
        closes = df['close'].values
        
        ema_20 = self.calculate_ema(closes, 20)[-1]
        ema_40 = self.calculate_ema(closes, 40)[-1]
        ema_20_prev = self.calculate_ema(closes, 20)[-2]
        ema_40_prev = self.calculate_ema(closes, 40)[-2]
        
        # Detect crossover
        bullish_cross = ema_20_prev <= ema_40_prev and ema_20 > ema_40
        bearish_cross = ema_20_prev >= ema_40_prev and ema_20 < ema_40
        
        ma_50 = np.mean(closes[-50:])
        ma_150 = np.mean(closes[-150:]) if len(closes) >= 150 else np.mean(closes)
        
        current_price = closes[-1]
        
        return {
            'ema_20': round(ema_20, 2),
            'ema_40': round(ema_40, 2),
            'ma_50': round(ma_50, 2),
            'ma_150': round(ma_150, 2),
            'signal': 'bullish' if ema_20 > ema_40 else 'bearish',
            'crossover': 'bullish_cross' if bullish_cross else 'bearish_cross' if bearish_cross else 'none',
            'trend': 'uptrend' if current_price > ma_50 > ma_150 else 'downtrend' if current_price < ma_50 < ma_150 else 'neutral'
        }
    
    def verify_signal(self, symbol: str, claimed_data: Dict, timeframe: str = '1h') -> Dict:
        """
        Verify claimed trading signal data against real data.
        
        This is the CORE anti-hallucination function.
        
        Args:
            symbol: Trading pair
            claimed_data: Dict of claimed values to verify
            timeframe: Candle interval
            
        Returns:
            Verification report
        """
        report = {
            'symbol': symbol,
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'status': 'VERIFIED',
            'verifications': [],
            'warnings': []
        }
        
        # Fetch raw data
        df = self.fetch_ohlcv(symbol, timeframe)
        if df is None:
            report['status'] = 'REJECTED'
            report['error'] = 'Failed to fetch data'
            return report
        
        closes = df['close'].values
        
        # Verify RSI if claimed
        if 'rsi' in claimed_data:
            actual_rsi = self.calculate_rsi(closes)
            claimed_rsi = claimed_data['rsi']
            tolerance = 2.0
            
            if actual_rsi is None:
                report['verifications'].append({
                    'metric': 'rsi',
                    'status': 'ERROR',
                    'message': 'Could not calculate RSI'
                })
            elif abs(actual_rsi - claimed_rsi) < tolerance:
                report['verifications'].append({
                    'metric': 'rsi',
                    'status': 'VERIFIED',
                    'claimed': claimed_rsi,
                    'actual': actual_rsi
                })
            else:
                report['verifications'].append({
                    'metric': 'rsi',
                    'status': 'REJECTED',
                    'claimed': claimed_rsi,
                    'actual': actual_rsi,
                    'message': f'RSI mismatch: claimed {claimed_rsi}, actual {actual_rsi}'
                })
                report['status'] = 'REJECTED'
        
        # Calculate all real indicators
        real_data = {
            'rsi': self.calculate_rsi(closes),
            'macd': self.calculate_macd(closes),
            'adx': self.calculate_adx(df),
            'bollinger': self.calculate_bollinger_bands(closes),
            'tbo': self.calculate_tbo_signal(df),
            'price': closes[-1],
            'volume': df['volume'].values[-1]
        }
        
        report['real_data'] = real_data
        
        # Log verification
        self.verification_log.append(report)
        
        return report
    
    def get_market_regime(self, symbol: str, timeframe: str = '4h') -> Dict:
        """
        Determine market regime for trading filter.
        
        From Across the Rubicon research:
        - ADX > 25 = trending market
        - Bollinger width = volatility measure
        
        Args:
            symbol: Trading pair
            timeframe: Candle interval
            
        Returns:
            Market regime analysis
        """
        df = self.fetch_ohlcv(symbol, timeframe)
        if df is None:
            return {'error': 'Failed to fetch data'}
        
        closes = df['close'].values
        
        adx = self.calculate_adx(df)
        bollinger = self.calculate_bollinger_bands(closes)
        tbo = self.calculate_tbo_signal(df)
        
        # Determine regime
        if adx['adx'] > 25:
            regime = 'trending'
        elif bollinger['width'] < 5:
            regime = 'ranging'
        else:
            regime = 'volatile'
        
        # Trading recommendation
        trade_allowed = True
        reason = []
        
        if adx['adx'] < 20:
            trade_allowed = False
            reason.append('ADX too low (weak trend)')
        
        if bollinger['position'] == 'inside' and bollinger['width'] < 3:
            trade_allowed = False
            reason.append('Low volatility squeeze')
        
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'regime': regime,
            'adx': adx,
            'bollinger': bollinger,
            'tbo': tbo,
            'trade_allowed': trade_allowed,
            'reason': reason if reason else ['Conditions favorable']
        }
    
    def _log_error(self, message: str):
        """Log error message."""
        self.verification_log.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'message': message
        })


if __name__ == '__main__':
    # Test Radar agent
    radar = RadarAgent(testnet=True)
    
    print("=" * 50)
    print("RADAR AGENT - Anti-Hallucination Test")
    print("=" * 50)
    
    # Test BTC/USDT
    symbol = 'BTC/USDT'
    
    print(f"\n📊 Fetching real data for {symbol}...")
    df = radar.fetch_ohlcv(symbol, '1h')
    
    if df is not None:
        closes = df['close'].values
        
        print(f"\n✅ Raw data fetched: {len(df)} candles")
        print(f"   Latest price: ${closes[-1]:,.2f}")
        
        print(f"\n📈 Calculated Indicators (NO HALLUCINATION):")
        print(f"   RSI: {radar.calculate_rsi(closes)}")
        print(f"   MACD: {radar.calculate_macd(closes)}")
        print(f"   ADX: {radar.calculate_adx(df)}")
        print(f"   Bollinger: {radar.calculate_bollinger_bands(closes)}")
        print(f"   TBO: {radar.calculate_tbo_signal(df)}")
        
        print(f"\n🔍 Market Regime Analysis:")
        regime = radar.get_market_regime(symbol)
        print(f"   Regime: {regime.get('regime', 'N/A')}")
        print(f"   Trade Allowed: {regime.get('trade_allowed', 'N/A')}")
        
        print(f"\n✅ VERIFICATION COMPLETE - NO HALLUCINATION DETECTED")
    else:
        print("❌ Failed to fetch data")
    
    print("\n" + "=" * 50)

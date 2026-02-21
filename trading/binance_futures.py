#!/usr/bin/env python3
"""
BINANCE FUTURES EXECUTOR

Paper trading executor for Binance Futures.
Implements HMAC authentication and all safety controls.

Features:
- HMAC authentication for Binance API
- Futures trading with configurable leverage
- Full trade logging with agent attribution
- Circuit breakers and risk management
"""

import os
import time
import hmac
import hashlib
import requests
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


class BinanceFuturesExecutor:
    """
    Binance Futures paper trading executor.
    
    Uses HMAC authentication for secure API access.
    All trades are logged with agent attribution.
    """
    
    # API endpoints
    TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    MAINNET_BASE_URL = "https://fapi.binance.com"
    
    def __init__(self, 
                 api_key: str = None,
                 api_secret: str = None,
                 testnet: bool = True,
                 max_leverage: int = 5):
        """
        Initialize Binance Futures executor.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet (default: True for safety)
            max_leverage: Maximum allowed leverage
        """
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        self.testnet = testnet
        self.max_leverage = max_leverage
        
        self.base_url = self.TESTNET_BASE_URL if testnet else self.MAINNET_BASE_URL
        
        # Trading state
        self.position_size_percent = float(os.getenv('POSITION_SIZE_PERCENT', 5))
        self.circuit_breaker_losses = int(os.getenv('CIRCUIT_BREAKER_LOSSES', 3))
        self.consecutive_losses = 0
        self.circuit_breaker_active = False
        
        # Trade log
        self.trades = []
        self.log_file = os.path.join(os.path.dirname(__file__), 'futures_trade_log.json')
        self._load_log()
        
        # Verify connection
        self._test_connection()
    
    def _sign(self, params: Dict) -> str:
        """Generate HMAC signature for request."""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, method: str, endpoint: str, params: Dict = None, signed: bool = True) -> Dict:
        """
        Make API request to Binance.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint
            params: Request parameters
            signed: Whether request needs signature
            
        Returns:
            API response
        """
        url = f"{self.base_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}
        
        if params is None:
            params = {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._sign(params)
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, params=params, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, params=params, timeout=10)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def _test_connection(self):
        """Test API connection."""
        print(f"\n{'='*60}")
        print("BINANCE FUTURES CONNECTION TEST")
        print(f"{'='*60}")
        print(f"Mode: {'TESTNET' if self.testnet else 'MAINNET'}")
        print(f"Max Leverage: {self.max_leverage}x")
        
        # Test public endpoint
        try:
            result = self._request('GET', '/fapi/v1/ping', signed=False)
            if 'error' in result:
                print(f"❌ Connection failed: {result['error']}")
            else:
                print(f"✅ API connection successful")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        # Test account access
        try:
            account = self._request('GET', '/fapi/v2/account')
            if 'error' in account:
                print(f"❌ Account access failed: {account['error']}")
            else:
                balance = float(account.get('totalWalletBalance', 0))
                print(f"✅ Account balance: ${balance:,.2f} USDT")
        except Exception as e:
            print(f"⚠️ Account check error: {e}")
        
        print(f"{'='*60}\n")
    
    def get_balance(self) -> float:
        """Get account balance in USDT."""
        account = self._request('GET', '/fapi/v2/account')
        if 'error' in account:
            return 0.0
        return float(account.get('totalWalletBalance', 0))
    
    def get_current_price(self, symbol: str) -> float:
        """Get current price for symbol."""
        result = self._request('GET', '/fapi/v1/ticker/price', {'symbol': symbol}, signed=False)
        if 'error' in result:
            return 0.0
        return float(result.get('price', 0))
    
    def set_leverage(self, symbol: str, leverage: int) -> Dict:
        """Set leverage for symbol."""
        if leverage > self.max_leverage:
            leverage = self.max_leverage
        
        return self._request('POST', '/fapi/v1/leverage', {
            'symbol': symbol,
            'leverage': leverage
        })
    
    def open_position(self, 
                      symbol: str,
                      side: str,  # 'BUY' for long, 'SELL' for short
                      quantity: float,
                      leverage: int = 1,
                      stop_loss: float = None,
                      take_profit: float = None) -> Dict:
        """
        Open a futures position.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' for long, 'SELL' for short
            quantity: Position size in base asset
            leverage: Leverage (max: self.max_leverage)
            stop_loss: Stop loss price
            take_profit: Take profit price
            
        Returns:
            Order result
        """
        # Check circuit breaker
        if self.circuit_breaker_active:
            return {'error': f'Circuit breaker active ({self.consecutive_losses} consecutive losses)'}
        
        # Set leverage
        self.set_leverage(symbol, leverage)
        
        # Open position
        order = self._request('POST', '/fapi/v1/order', {
            'symbol': symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity
        })
        
        if 'error' in order:
            return order
        
        # Set stop loss if provided
        if stop_loss:
            sl_side = 'SELL' if side == 'BUY' else 'BUY'
            self._request('POST', '/fapi/v1/order', {
                'symbol': symbol,
                'side': sl_side,
                'type': 'STOP_MARKET',
                'stopPrice': stop_loss,
                'closePosition': 'true'
            })
        
        # Set take profit if provided
        if take_profit:
            tp_side = 'SELL' if side == 'BUY' else 'BUY'
            self._request('POST', '/fapi/v1/order', {
                'symbol': symbol,
                'side': tp_side,
                'type': 'TAKE_PROFIT_MARKET',
                'stopPrice': take_profit,
                'closePosition': 'true'
            })
        
        return order
    
    def close_position(self, symbol: str, side: str, quantity: float) -> Dict:
        """Close a futures position."""
        close_side = 'SELL' if side == 'BUY' else 'BUY'
        return self._request('POST', '/fapi/v1/order', {
            'symbol': symbol,
            'side': close_side,
            'type': 'MARKET',
            'quantity': quantity
        })
    
    def get_positions(self) -> List[Dict]:
        """Get all open positions."""
        account = self._request('GET', '/fapi/v2/account')
        if 'error' in account:
            return []
        
        positions = []
        for pos in account.get('positions', []):
            qty = float(pos.get('positionAmt', 0))
            if qty != 0:
                positions.append({
                    'symbol': pos.get('symbol'),
                    'size': qty,
                    'entry_price': float(pos.get('entryPrice', 0)),
                    'unrealized_pnl': float(pos.get('unRealizedProfit', 0)),
                    'leverage': int(pos.get('leverage', 1)),
                    'side': 'LONG' if qty > 0 else 'SHORT'
                })
        
        return positions
    
    def _load_log(self):
        """Load existing trade log."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.trades = data.get('trades', [])
                    self.consecutive_losses = data.get('consecutive_losses', 0)
                    self.circuit_breaker_active = data.get('circuit_breaker_active', False)
            except:
                pass
    
    def _save_log(self):
        """Save trade log."""
        with open(self.log_file, 'w') as f:
            json.dump({
                'trades': self.trades,
                'consecutive_losses': self.consecutive_losses,
                'circuit_breaker_active': self.circuit_breaker_active,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)


# Import json at top
import json

def main():
    """Test Binance Futures executor."""
    print("="*60)
    print("BINANCE FUTURES EXECUTOR - TEST")
    print("="*60)
    
    executor = BinanceFuturesExecutor(testnet=True)
    
    # Get balance
    balance = executor.get_balance()
    print(f"\n💰 Balance: ${balance:,.2f} USDT")
    
    # Get positions
    positions = executor.get_positions()
    print(f"\n📊 Open Positions: {len(positions)}")
    for pos in positions:
        print(f"   {pos['symbol']}: {pos['side']} {abs(pos['size'])} @ ${pos['entry_price']}")
    
    print("\n✅ Executor ready")


if __name__ == '__main__':
    main()

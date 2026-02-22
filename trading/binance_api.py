#!/usr/bin/env python3
"""
Binance Testnet API - Clean JSON wrapper
Uses direct API calls bypassing banner output
"""
import sys
import os
import json
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

# Load credentials
def load_env():
    env_path = '/Users/michaelnetto/.openclaw/workspace/trading/.env'
    env = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
    return env

ENV = load_env()
API_KEY = ENV.get('BINANCE_API_KEY', '')
API_SECRET = ENV.get('BINANCE_API_SECRET', '')
BASE_URL = 'https://testnet.binancefuture.com'

def sign(params):
    query = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return signature

def request(endpoint, params=None, method='GET'):
    if params is None:
        params = {}
    
    headers = {'X-MBX-APIKEY': API_KEY}
    params['timestamp'] = int(time.time() * 1000)
    params['signature'] = sign(params)
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            resp = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == 'POST':
            resp = requests.post(url, headers=headers, params=params, timeout=10)
        else:
            return {'error': f'Unknown method: {method}'}
        
        return resp.json()
    except Exception as e:
        return {'error': str(e)}

def get_positions():
    """Get open futures positions"""
    account = request('/fapi/v2/account')
    
    if 'error' in account:
        return account
    
    positions = []
    for pos in account.get('positions', []):
        size = float(pos.get('positionAmt', 0))
        if size != 0:
            positions.append({
                'symbol': pos.get('symbol', ''),
                'side': 'LONG' if size > 0 else 'SHORT',
                'size': abs(size),
                'entry_price': float(pos.get('entryPrice', 0)),
                'unrealized_pnl': float(pos.get('unRealizedProfit', 0)),
                'leverage': int(pos.get('leverage', 1))
            })
    
    return positions

def get_balance():
    """Get account balance in USDT"""
    account = request('/fapi/v2/account')
    
    if 'error' in account:
        return 0
    
    return float(account.get('totalWalletBalance', 0))

def get_price(symbol):
    """Get current price for symbol"""
    try:
        resp = requests.get(f"{BASE_URL}/fapi/v1/ticker/price", params={'symbol': symbol}, timeout=10)
        return float(resp.json().get('price', 0))
    except:
        return 0

def main():
    command = sys.argv[1] if len(sys.argv) > 1 else 'positions'
    
    if command == 'positions':
        result = get_positions()
    elif command == 'balance':
        result = {'balance': get_balance()}
    elif command == 'price':
        symbol = sys.argv[2] if len(sys.argv) > 2 else 'BTCUSDT'
        result = {'symbol': symbol, 'price': get_price(symbol)}
    else:
        result = {'error': f'Unknown command: {command}'}
    
    print(json.dumps(result))

if __name__ == '__main__':
    main()
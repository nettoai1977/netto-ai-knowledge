#!/usr/bin/env python3
"""
Execute paper trades on Binance Testnet
"""
import sys
sys.path.insert(0, '/Users/michaelnetto/.openclaw/workspace/trading')

from binance_futures import BinanceFuturesExecutor

def main():
    print("="*60)
    print("EXECUTING PAPER TRADES ON BINANCE TESTNET")
    print("="*60)
    
    executor = BinanceFuturesExecutor(testnet=True)
    
    # TRD-001: ADA/USDT SHORT
    print("\n📈 TRD-001: ADA/USDT SHORT")
    print("-"*40)
    
    # Get current price
    ada_price = executor.get_current_price("ADAUSDT")
    print(f"Current ADA Price: ${ada_price}")
    
    # Calculate position size (2% of $5000 = $100)
    position_size_usd = 100
    ada_quantity = round(position_size_usd / ada_price, 0)  # Round to whole ADA
    
    # Set leverage
    executor.set_leverage("ADAUSDT", 3)
    
    # Execute SHORT
    result = executor.open_position(
        symbol="ADAUSDT",
        side="SELL",
        quantity=int(ada_quantity),
        leverage=3,
        stop_loss=ada_price * 1.0047,  # 0.47% above entry
        take_profit=ada_price * 0.9905  # 0.95% below entry
    )
    
    if 'error' in result:
        print(f"❌ TRD-001 Failed: {result['error']}")
    else:
        print(f"✅ TRD-001 Executed: Order ID {result.get('orderId', 'N/A')}")
        print(f"   Quantity: {ada_quantity} ADA")
        print(f"   Entry: ${ada_price}")
    
    # TRD-002: AVAX/USDT SHORT
    print("\n📈 TRD-002: AVAX/USDT SHORT")
    print("-"*40)
    
    avax_price = executor.get_current_price("AVAXUSDT")
    print(f"Current AVAX Price: ${avax_price}")
    
    avax_quantity = round(position_size_usd / avax_price, 1)  # 1 decimal
    
    executor.set_leverage("AVAXUSDT", 3)
    
    result = executor.open_position(
        symbol="AVAXUSDT",
        side="SELL",
        quantity=avax_quantity,
        leverage=3,
        stop_loss=avax_price * 1.0053,  # 0.53% above entry
        take_profit=avax_price * 0.9895  # 1.05% below entry
    )
    
    if 'error' in result:
        print(f"❌ TRD-002 Failed: {result['error']}")
    else:
        print(f"✅ TRD-002 Executed: Order ID {result.get('orderId', 'N/A')}")
        print(f"   Quantity: {avax_quantity} AVAX")
        print(f"   Entry: ${avax_price}")
    
    # Show positions
    print("\n" + "="*60)
    print("OPEN POSITIONS ON BINANCE TESTNET")
    print("="*60)
    
    positions = executor.get_positions()
    if not positions:
        print("No open positions")
    else:
        for pos in positions:
            pnl_str = f"${pos['unrealized_pnl']:+,.2f}"
            print(f"{pos['symbol']}: {pos['side']} {abs(pos['size'])} @ ${pos['entry_price']:,.2f} | PnL: {pnl_str}")

if __name__ == '__main__':
    main()
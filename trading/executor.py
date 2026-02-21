#!/usr/bin/env python3
"""
PAPER TRADE EXECUTOR

Captures every trade decision, logs rationale, tracks P&L.
Implements circuit breakers and risk management.

Based on research from:
- Michael Automates: Backtest-first approach
- Aaron Dishner: TBO signals, new listings
- Across the Rubicon: Circuit breakers, position sizing
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class TradeStatus(Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class TradeAction(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass
class Trade:
    """Represents a single trade."""
    
    # Identification
    trade_id: str
    symbol: str
    action: str  # LONG or SHORT
    
    # Decision data
    timestamp_open: str
    entry_price: float
    position_size: float  # USDT
    stop_loss: float
    take_profit: float
    
    # Ensemble data
    ensemble_signal: str
    ensemble_confidence: float
    ensemble_agreement: float
    confluence_score: float
    
    # Agent votes
    atlas_vote: str
    atlas_confidence: float
    nova_vote: str
    nova_confidence: float
    orion_vote: str
    orion_confidence: float
    flash_vote: str
    flash_confidence: float
    
    # Rationale
    rationale: str
    
    # Market conditions at entry
    regime: str
    rsi: float
    adx: float
    tbo_signal: str
    
    # Status
    status: str = "OPEN"
    
    # Exit data (filled when closed)
    timestamp_close: Optional[str] = None
    exit_price: Optional[float] = None
    pnl_usd: Optional[float] = None
    pnl_percent: Optional[float] = None
    close_reason: Optional[str] = None
    hold_duration_minutes: Optional[float] = None


@dataclass
class TradeLog:
    """Complete trade log with performance metrics."""
    
    trades: List[Dict]
    total_trades: int
    open_trades: int
    closed_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl_usd: float
    total_pnl_percent: float
    avg_win_usd: float
    avg_loss_usd: float
    max_drawdown: float
    sharpe_ratio: float


class PaperTradeExecutor:
    """
    Paper trade executor with full logging and risk management.
    
    Features:
    - Captures every trade decision with rationale
    - Implements circuit breaker (3 losses = stop)
    - Position sizing (5% max per trade)
    - Tracks all agent votes
    - Calculates performance metrics
    - NO real money involved
    """
    
    def __init__(self, 
                 initial_capital: float = 10000.0,
                 max_position_percent: float = 5.0,
                 max_drawdown_percent: float = 50.0,
                 circuit_breaker_losses: int = 3):
        """
        Initialize paper trade executor.
        
        Args:
            initial_capital: Starting capital in USDT
            max_position_percent: Max % of capital per trade
            max_drawdown_percent: Max drawdown before stopping
            circuit_breaker_losses: Consecutive losses before circuit breaker
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_position_percent = max_position_percent
        self.max_drawdown_percent = max_drawdown_percent
        self.circuit_breaker_losses = circuit_breaker_losses
        
        self.trades: List[Trade] = []
        self.consecutive_losses = 0
        self.circuit_breaker_active = False
        
        self.log_file = os.path.join(os.path.dirname(__file__), 'trade_log.json')
        self.load_log()
    
    def load_log(self):
        """Load existing trade log."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.trades = [Trade(**t) for t in data.get('trades', [])]
                    self.current_capital = data.get('current_capital', self.initial_capital)
                    self.consecutive_losses = data.get('consecutive_losses', 0)
                    self.circuit_breaker_active = data.get('circuit_breaker_active', False)
            except:
                pass
    
    def save_log(self):
        """Save trade log to file."""
        data = {
            'metadata': {
                'initial_capital': self.initial_capital,
                'current_capital': self.current_capital,
                'consecutive_losses': self.consecutive_losses,
                'circuit_breaker_active': self.circuit_breaker_active,
                'last_updated': datetime.now().isoformat()
            },
            'performance': self.get_performance_summary(),
            'trades': [asdict(t) for t in self.trades]
        }
        
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def can_open_trade(self) -> tuple:
        """
        Check if new trades can be opened.
        
        Returns:
            (can_trade: bool, reason: str)
        """
        if self.circuit_breaker_active:
            return False, f"Circuit breaker active ({self.consecutive_losses} consecutive losses)"
        
        open_trades = len([t for t in self.trades if t.status == "OPEN"])
        if open_trades >= 5:
            return False, "Max open trades (5) reached"
        
        drawdown = (self.initial_capital - self.current_capital) / self.initial_capital * 100
        if drawdown >= self.max_drawdown_percent:
            return False, f"Max drawdown reached ({drawdown:.1f}%)"
        
        return True, "Can open trade"
    
    def calculate_position_size(self) -> float:
        """Calculate position size based on risk rules."""
        max_position = self.current_capital * (self.max_position_percent / 100)
        return round(max_position, 2)
    
    def execute_trade(self, 
                      symbol: str,
                      action: str,
                      entry_price: float,
                      ensemble_result: Dict,
                      scan_result: Dict,
                      regime_data: Dict) -> Optional[Trade]:
        """
        Execute a paper trade.
        
        Args:
            symbol: Trading pair
            action: LONG or SHORT
            entry_price: Entry price
            ensemble_result: Ensemble analysis result
            scan_result: Scanner result
            regime_data: Market regime data
            
        Returns:
            Trade object if executed, None if blocked
        """
        # Check if can trade
        can_trade, reason = self.can_open_trade()
        if not can_trade:
            print(f"❌ TRADE BLOCKED: {reason}")
            return None
        
        # Calculate position size
        position_size = self.calculate_position_size()
        
        # Get ensemble votes
        votes = ensemble_result.votes if hasattr(ensemble_result, 'votes') else []
        vote_dict = {v.agent_name.lower(): v for v in votes}
        
        # Calculate stop loss and take profit (2% SL, 4% TP = 1:2 R:R)
        if action == "LONG":
            stop_loss = entry_price * 0.98
            take_profit = entry_price * 1.04
        else:
            stop_loss = entry_price * 1.02
            take_profit = entry_price * 0.96
        
        # Build rationale
        rationale = self._build_rationale(ensemble_result, scan_result, regime_data)
        
        # Create trade
        trade = Trade(
            trade_id=str(uuid.uuid4())[:8],
            symbol=symbol,
            action=action,
            timestamp_open=datetime.now().isoformat(),
            entry_price=entry_price,
            position_size=position_size,
            stop_loss=stop_loss,
            take_profit=take_profit,
            ensemble_signal=ensemble_result.signal.value if hasattr(ensemble_result, 'signal') else 'WAIT',
            ensemble_confidence=ensemble_result.confidence if hasattr(ensemble_result, 'confidence') else 0,
            ensemble_agreement=ensemble_result.agreement_ratio if hasattr(ensemble_result, 'agreement_ratio') else 0,
            confluence_score=scan_result.get('confluence_score', 0),
            atlas_vote=vote_dict.get('atlas', vote_dict.get('Atlas', None)).signal.value if vote_dict.get('atlas', vote_dict.get('Atlas')) else 'N/A',
            atlas_confidence=vote_dict.get('atlas', vote_dict.get('Atlas', None)).confidence if vote_dict.get('atlas', vote_dict.get('Atlas')) else 0,
            nova_vote=vote_dict.get('nova', vote_dict.get('Nova', None)).signal.value if vote_dict.get('nova', vote_dict.get('Nova')) else 'N/A',
            nova_confidence=vote_dict.get('nova', vote_dict.get('Nova', None)).confidence if vote_dict.get('nova', vote_dict.get('Nova')) else 0,
            orion_vote=vote_dict.get('orion', vote_dict.get('Orion', None)).signal.value if vote_dict.get('orion', vote_dict.get('Orion')) else 'N/A',
            orion_confidence=vote_dict.get('orion', vote_dict.get('Orion', None)).confidence if vote_dict.get('orion', vote_dict.get('Orion')) else 0,
            flash_vote=vote_dict.get('flash', vote_dict.get('Flash', None)).signal.value if vote_dict.get('flash', vote_dict.get('Flash')) else 'N/A',
            flash_confidence=vote_dict.get('flash', vote_dict.get('Flash', None)).confidence if vote_dict.get('flash', vote_dict.get('Flash')) else 0,
            rationale=rationale,
            regime=regime_data.get('regime', 'unknown'),
            rsi=regime_data.get('real_data', {}).get('rsi', 0) if 'real_data' in regime_data else regime_data.get('rsi', 0),
            adx=regime_data.get('adx', {}).get('adx', 0) if 'adx' in regime_data else 0,
            tbo_signal=regime_data.get('tbo', {}).get('signal', 'unknown') if 'tbo' in regime_data else 'unknown',
            status="OPEN"
        )
        
        self.trades.append(trade)
        self.save_log()
        
        print(f"\n{'='*70}")
        print(f"📝 TRADE OPENED: {trade.trade_id}")
        print(f"{'='*70}")
        print(f"Symbol: {symbol}")
        print(f"Action: {action}")
        print(f"Entry: ${entry_price:,.2f}")
        print(f"Position: ${position_size:,.2f} ({self.max_position_percent}% of capital)")
        print(f"Stop Loss: ${stop_loss:,.2f}")
        print(f"Take Profit: ${take_profit:,.2f}")
        print(f"Ensemble: {trade.ensemble_signal} ({trade.ensemble_confidence:.1f}%)")
        print(f"Confluence: {trade.confluence_score}%")
        print(f"Rationale: {rationale[:100]}...")
        print(f"{'='*70}\n")
        
        return trade
    
    def close_trade(self, 
                    trade_id: str, 
                    exit_price: float, 
                    reason: str = "Manual close") -> Optional[Trade]:
        """
        Close a paper trade.
        
        Args:
            trade_id: Trade ID to close
            exit_price: Exit price
            reason: Reason for closing
            
        Returns:
            Closed trade
        """
        trade = next((t for t in self.trades if t.trade_id == trade_id), None)
        if not trade:
            print(f"❌ Trade {trade_id} not found")
            return None
        
        if trade.status != "OPEN":
            print(f"❌ Trade {trade_id} already {trade.status}")
            return None
        
        # Calculate P&L
        if trade.action == "LONG":
            pnl_percent = (exit_price - trade.entry_price) / trade.entry_price * 100
        else:
            pnl_percent = (trade.entry_price - exit_price) / trade.entry_price * 100
        
        pnl_usd = trade.position_size * (pnl_percent / 100)
        
        # Update capital
        self.current_capital += pnl_usd
        
        # Update trade
        trade.status = "CLOSED"
        trade.timestamp_close = datetime.now().isoformat()
        trade.exit_price = exit_price
        trade.pnl_usd = round(pnl_usd, 2)
        trade.pnl_percent = round(pnl_percent, 2)
        trade.close_reason = reason
        
        # Calculate hold duration
        if trade.timestamp_open:
            t_open = datetime.fromisoformat(trade.timestamp_open)
            t_close = datetime.fromisoformat(trade.timestamp_close)
            trade.hold_duration_minutes = (t_close - t_open).total_seconds() / 60
        
        # Update circuit breaker
        if pnl_usd < 0:
            self.consecutive_losses += 1
            if self.consecutive_losses >= self.circuit_breaker_losses:
                self.circuit_breaker_active = True
                print(f"\n🚨 CIRCUIT BREAKER ACTIVATED ({self.consecutive_losses} consecutive losses)")
        else:
            self.consecutive_losses = 0
        
        self.save_log()
        
        result_emoji = "✅" if pnl_usd > 0 else "❌"
        print(f"\n{'='*70}")
        print(f"{result_emoji} TRADE CLOSED: {trade_id}")
        print(f"{'='*70}")
        print(f"Symbol: {trade.symbol}")
        print(f"Entry: ${trade.entry_price:,.2f}")
        print(f"Exit: ${exit_price:,.2f}")
        print(f"P&L: ${pnl_usd:+,.2f} ({pnl_percent:+.2f}%)")
        print(f"Duration: {trade.hold_duration_minutes:.1f} minutes")
        print(f"Reason: {reason}")
        print(f"Capital: ${self.current_capital:,.2f}")
        print(f"{'='*70}\n")
        
        return trade
    
    def _build_rationale(self, ensemble_result, scan_result, regime_data) -> str:
        """Build trade rationale string."""
        parts = []
        
        # Ensemble
        if hasattr(ensemble_result, 'signal'):
            parts.append(f"Ensemble voted {ensemble_result.signal.value}")
            parts.append(f"with {ensemble_result.agreement_ratio*100:.0f}% agreement")
        
        # Confluence
        confluence = scan_result.get('confluence_score', 0)
        parts.append(f"Confluence: {confluence}%")
        
        # Market conditions
        regime = regime_data.get('regime', 'unknown')
        rsi = regime_data.get('real_data', {}).get('rsi', 0) if 'real_data' in regime_data else regime_data.get('rsi', 0)
        adx = regime_data.get('adx', {}).get('adx', 0) if 'adx' in regime_data else 0
        
        parts.append(f"Regime: {regime}")
        parts.append(f"RSI: {rsi:.1f}")
        parts.append(f"ADX: {adx:.1f}")
        
        return " | ".join(parts)
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary."""
        closed_trades = [t for t in self.trades if t.status == "CLOSED"]
        winning_trades = [t for t in closed_trades if t.pnl_usd and t.pnl_usd > 0]
        losing_trades = [t for t in closed_trades if t.pnl_usd and t.pnl_usd <= 0]
        
        total_pnl = sum(t.pnl_usd or 0 for t in closed_trades)
        total_trades = len(closed_trades)
        
        win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
        avg_win = sum(t.pnl_usd or 0 for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t.pnl_usd or 0 for t in losing_trades) / len(losing_trades) if losing_trades else 0
        
        # Calculate max drawdown
        peak = self.initial_capital
        max_dd = 0
        for t in closed_trades:
            if t.pnl_usd:
                peak += t.pnl_usd
                dd = (peak - self.initial_capital) / self.initial_capital * 100
                max_dd = min(max_dd, dd)
        
        return {
            'initial_capital': self.initial_capital,
            'current_capital': round(self.current_capital, 2),
            'total_return': round((self.current_capital - self.initial_capital) / self.initial_capital * 100, 2),
            'total_trades': total_trades,
            'open_trades': len([t for t in self.trades if t.status == "OPEN"]),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': round(win_rate, 2),
            'total_pnl_usd': round(total_pnl, 2),
            'avg_win_usd': round(avg_win, 2),
            'avg_loss_usd': round(avg_loss, 2),
            'max_drawdown': round(max_dd, 2),
            'circuit_breaker_active': self.circuit_breaker_active,
            'consecutive_losses': self.consecutive_losses
        }
    
    def print_summary(self):
        """Print performance summary."""
        perf = self.get_performance_summary()
        
        print(f"\n{'='*70}")
        print("📊 PERFORMANCE SUMMARY")
        print(f"{'='*70}")
        print(f"Initial Capital: ${perf['initial_capital']:,.2f}")
        print(f"Current Capital: ${perf['current_capital']:,.2f}")
        print(f"Total Return: {perf['total_return']:+.2f}%")
        print(f"\nTotal Trades: {perf['total_trades']}")
        print(f"Open Trades: {perf['open_trades']}")
        print(f"Winning: {perf['winning_trades']} | Losing: {perf['losing_trades']}")
        print(f"Win Rate: {perf['win_rate']:.1f}%")
        print(f"\nTotal P&L: ${perf['total_pnl_usd']:+,.2f}")
        print(f"Avg Win: ${perf['avg_win_usd']:+,.2f}")
        print(f"Avg Loss: ${perf['avg_loss_usd']:,.2f}")
        print(f"Max Drawdown: {perf['max_drawdown']:.2f}%")
        
        if perf['circuit_breaker_active']:
            print(f"\n🚨 CIRCUIT BREAKER ACTIVE")
        
        print(f"{'='*70}\n")


def main():
    """Test paper trade executor."""
    print("="*70)
    print("PAPER TRADE EXECUTOR - TEST")
    print("="*70)
    
    executor = PaperTradeExecutor(
        initial_capital=10000.0,
        max_position_percent=5.0,
        circuit_breaker_losses=3
    )
    
    # Print current status
    executor.print_summary()
    
    # Show log file location
    print(f"📁 Trade log: {executor.log_file}")
    
    print("\n✅ Executor ready to capture trades")


if __name__ == '__main__':
    main()

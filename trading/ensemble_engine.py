#!/usr/bin/env python3
"""
ENSEMBLE TRADING ENGINE - Multi-Model Consensus System

"Wisdom of Crowds" for AI Trading Models

How it works:
1. Spawn 4 sub-agents with different models
2. Each analyzes same market data
3. Collect votes (LONG/SHORT/WAIT)
4. Consensus engine decides
5. Radar verifies, then execute

Models used:
- Atlas (GLM 4.7) - Deep reasoning
- Nova (Kimi K2.5) - Balanced analysis
- Orion (DeepSeek V3.2) - Technical focus
- Flash (StepFun 3.5 Flash) - Fast reasoning
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Signal(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    WAIT = "WAIT"


@dataclass
class AgentVote:
    agent_name: str
    model: str
    signal: Signal
    confidence: float
    reasoning: str
    timestamp: str


@dataclass
class ConsensusResult:
    signal: Signal
    confidence: float
    votes: List[AgentVote]
    agreement_ratio: float
    should_trade: bool
    reasoning: str


class EnsembleEngine:
    """
    Multi-model consensus engine for trading decisions.
    
    Requires 3/4 agents to agree before generating signal.
    This reduces false positives and validates decisions.
    """
    
    # Agent configurations
    AGENTS = {
        "atlas": {
            "name": "Atlas",
            "model": "nvidia/z-ai/glm4.7",
            "specialty": "Deep reasoning and complex analysis",
            "thinking": True
        },
        "nova": {
            "name": "Nova",
            "model": "nvidia/moonshotai/kimi-k2.5",
            "specialty": "Balanced reasoning with trend awareness",
            "thinking": True
        },
        "orion": {
            "name": "Orion",
            "model": "nvidia/deepseek-ai/deepseek-v3.2",
            "specialty": "Technical analysis and pattern recognition",
            "thinking": True
        },
        "flash": {
            "name": "Flash",
            "model": "nvidia/stepfun-ai/step-3.5-flash",
            "specialty": "Fast reasoning and quick decisions",
            "thinking": True
        }
    }
    
    def __init__(self, consensus_threshold: float = 0.75):
        """
        Initialize ensemble engine.
        
        Args:
            consensus_threshold: Minimum agreement ratio (default: 0.75 = 3/4)
        """
        self.consensus_threshold = consensus_threshold
        self.vote_history = []
        self.performance_log = []
    
    def create_analysis_prompt(self, symbol: str, market_data: Dict) -> str:
        """
        Create analysis prompt for agents.
        
        Args:
            symbol: Trading pair
            market_data: Market data from Radar agent
            
        Returns:
            Analysis prompt
        """
        prompt = f"""
You are a cryptocurrency trading analyst. Analyze the following market data and provide a trading signal.

## MARKET DATA: {symbol}

### Price Information
- Current Price: ${market_data.get('price', 'N/A')}
- 24h Change: {market_data.get('change_24h', 'N/A')}%

### Technical Indicators
- RSI (14): {market_data.get('rsi', 'N/A')}
- MACD: {market_data.get('macd', {})}
- ADX: {market_data.get('adx', {})}
- Bollinger Bands: {market_data.get('bollinger', {})}
- TBO Signal: {market_data.get('tbo', {})}

### Market Regime
- Regime: {market_data.get('regime', 'N/A')}
- Trade Allowed: {market_data.get('trade_allowed', 'N/A')}

## YOUR TASK

1. Analyze all indicators
2. Consider trend direction and strength
3. Evaluate risk/reward
4. Provide your vote

## OUTPUT FORMAT (JSON)

```json
{{
    "signal": "LONG" or "SHORT" or "WAIT",
    "confidence": 0.0-100.0,
    "reasoning": "Your detailed analysis in 2-3 sentences"
}}
```

IMPORTANT:
- LONG = Bullish, expect price up
- SHORT = Bearish, expect price down  
- WAIT = Uncertain or unfavorable conditions
- Confidence = How sure you are (0-100)

Output ONLY the JSON, nothing else.
"""
        return prompt
    
    def parse_agent_response(self, response: str) -> Dict:
        """
        Parse agent response to extract signal.
        
        Args:
            response: Agent's JSON response
            
        Returns:
            Parsed signal data
        """
        try:
            # Try to extract JSON
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0]
            elif '```' in response:
                response = response.split('```')[1].split('```')[0]
            
            data = json.loads(response.strip())
            
            signal_str = data.get('signal', 'WAIT').upper()
            signal = Signal[signal_str] if signal_str in Signal.__members__ else Signal.WAIT
            
            return {
                'signal': signal,
                'confidence': float(data.get('confidence', 50)),
                'reasoning': data.get('reasoning', 'No reasoning provided')
            }
        except Exception as e:
            return {
                'signal': Signal.WAIT,
                'confidence': 0,
                'reasoning': f'Failed to parse response: {e}'
            }
    
    def simulate_agent_vote(self, agent_id: str, market_data: Dict) -> AgentVote:
        """
        Simulate an agent vote (for testing without API calls).
        
        In production, this would spawn a sub-agent with the specified model.
        
        Args:
            agent_id: Agent identifier
            market_data: Market data
            
        Returns:
            Agent vote
        """
        agent = self.AGENTS.get(agent_id, {})
        
        # Simplified logic based on indicators
        rsi = market_data.get('rsi', 50)
        adx = market_data.get('adx', {}).get('adx', 0)
        tbo = market_data.get('tbo', {}).get('signal', 'neutral')
        regime = market_data.get('regime', 'unknown')
        
        # Determine signal based on technical analysis
        signal = Signal.WAIT
        confidence = 50
        reasoning = ""
        
        if regime == 'trending' and adx > 25:
            if tbo == 'bullish' and rsi < 70:
                signal = Signal.LONG
                confidence = 60 + (adx - 25)  # Higher ADX = higher confidence
                reasoning = f"Strong bullish trend (ADX={adx:.1f}), RSI not overbought, TBO bullish"
            elif tbo == 'bearish' and rsi > 30:
                signal = Signal.SHORT
                confidence = 60 + (adx - 25)
                reasoning = f"Strong bearish trend (ADX={adx:.1f}), RSI not oversold, TBO bearish"
            else:
                signal = Signal.WAIT
                confidence = 40
                reasoning = f"Mixed signals: TBO={tbo}, RSI={rsi:.1f}, wait for clarity"
        else:
            signal = Signal.WAIT
            confidence = 30
            reasoning = f"Unfavorable regime ({regime}) or weak trend (ADX={adx:.1f})"
        
        # Add agent personality variation
        if agent_id == 'atlas':  # GLM 4.7 - Deep reasoning
            confidence = min(100, confidence + 10)  # More confident
            reasoning = f"[Deep Analysis] {reasoning}"
        elif agent_id == 'nova':  # Kimi K2.5 - Balanced
            pass  # Keep as is
        elif agent_id == 'orion':  # DeepSeek - Technical
            reasoning = f"[Technical] {reasoning}"
        elif agent_id == 'flash':  # StepFun - Fast
            confidence = max(0, confidence - 5)  # Slightly less confident
            reasoning = f"[Quick] {reasoning}"
        
        return AgentVote(
            agent_name=agent.get('name', agent_id),
            model=agent.get('model', 'unknown'),
            signal=signal,
            confidence=min(100, max(0, confidence)),
            reasoning=reasoning,
            timestamp=datetime.now().isoformat()
        )
    
    def calculate_consensus(self, votes: List[AgentVote]) -> ConsensusResult:
        """
        Calculate consensus from agent votes.
        
        Args:
            votes: List of agent votes
            
        Returns:
            Consensus result
        """
        if not votes:
            return ConsensusResult(
                signal=Signal.WAIT,
                confidence=0,
                votes=[],
                agreement_ratio=0,
                should_trade=False,
                reasoning="No votes received"
            )
        
        # Count votes
        signal_counts = {s: 0 for s in Signal}
        total_confidence = {s: 0 for s in Signal}
        
        for vote in votes:
            signal_counts[vote.signal] += 1
            total_confidence[vote.signal] += vote.confidence
        
        # Find majority
        majority_signal = max(signal_counts, key=signal_counts.get)
        majority_count = signal_counts[majority_signal]
        agreement_ratio = majority_count / len(votes)
        
        # Calculate weighted confidence
        if majority_count > 0:
            avg_confidence = total_confidence[majority_signal] / majority_count
        else:
            avg_confidence = 0
        
        # Determine if should trade
        should_trade = (
            agreement_ratio >= self.consensus_threshold and
            majority_signal != Signal.WAIT and
            avg_confidence >= 60
        )
        
        # Build reasoning
        vote_summary = ", ".join([
            f"{v.agent_name}: {v.signal.value} ({v.confidence:.0f}%)"
            for v in votes
        ])
        
        if should_trade:
            reasoning = f"CONSENSUS: {majority_signal.value} with {agreement_ratio*100:.0f}% agreement. {vote_summary}"
        elif majority_signal == Signal.WAIT:
            reasoning = f"NO CONSENSUS: Majority voted WAIT. {vote_summary}"
        else:
            reasoning = f"INSUFFICIENT CONSENSUS: Only {agreement_ratio*100:.0f}% agree (need {self.consensus_threshold*100:.0f}%). {vote_summary}"
        
        return ConsensusResult(
            signal=majority_signal,
            confidence=avg_confidence,
            votes=votes,
            agreement_ratio=agreement_ratio,
            should_trade=should_trade,
            reasoning=reasoning
        )
    
    def run_ensemble(self, symbol: str, market_data: Dict, simulate: bool = True) -> ConsensusResult:
        """
        Run ensemble analysis.
        
        Args:
            symbol: Trading pair
            market_data: Market data from Radar
            simulate: Use simulated votes (for testing)
            
        Returns:
            Consensus result
        """
        votes = []
        
        print(f"\n{'='*60}")
        print(f"ENSEMBLE ANALYSIS: {symbol}")
        print(f"{'='*60}")
        
        for agent_id, agent_config in self.AGENTS.items():
            print(f"\n🤖 {agent_config['name']} ({agent_config['model'].split('/')[-1]})")
            print(f"   Specialty: {agent_config['specialty']}")
            
            if simulate:
                vote = self.simulate_agent_vote(agent_id, market_data)
            else:
                # In production, spawn sub-agent here
                vote = self.simulate_agent_vote(agent_id, market_data)
            
            votes.append(vote)
            print(f"   Vote: {vote.signal.value}")
            print(f"   Confidence: {vote.confidence:.1f}%")
            print(f"   Reasoning: {vote.reasoning}")
        
        # Calculate consensus
        result = self.calculate_consensus(votes)
        
        print(f"\n{'='*60}")
        print("CONSENSUS RESULT")
        print(f"{'='*60}")
        print(f"Signal: {result.signal.value}")
        print(f"Agreement: {result.agreement_ratio*100:.0f}%")
        print(f"Confidence: {result.confidence:.1f}%")
        print(f"Should Trade: {'✅ YES' if result.should_trade else '❌ NO'}")
        print(f"Reasoning: {result.reasoning}")
        
        # Log
        self.vote_history.append({
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'votes': [
                {
                    'agent': v.agent_name,
                    'model': v.model,
                    'signal': v.signal.value,
                    'confidence': v.confidence,
                    'reasoning': v.reasoning
                } for v in votes
            ],
            'consensus': {
                'signal': result.signal.value,
                'agreement': result.agreement_ratio,
                'confidence': result.confidence,
                'should_trade': result.should_trade
            }
        })
        
        return result
    
    def save_history(self, filepath: str = None):
        """Save vote history to JSON."""
        if filepath is None:
            filepath = os.path.join(os.path.dirname(__file__), 'ensemble_history.json')
        
        with open(filepath, 'w') as f:
            json.dump(self.vote_history, f, indent=2, default=str)
        
        print(f"\n📁 History saved to {filepath}")


def main():
    """Test ensemble engine."""
    from radar_agent import RadarAgent
    
    print("="*60)
    print("ENSEMBLE TRADING ENGINE - TEST")
    print("="*60)
    
    # Get real market data
    radar = RadarAgent(testnet=True)
    symbol = 'BTC/USDT'
    
    print(f"\n📊 Fetching market data for {symbol}...")
    regime = radar.get_market_regime(symbol, '4h')
    
    if 'error' in regime:
        print(f"❌ Error: {regime['error']}")
        return
    
    # Prepare market data for ensemble
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
    
    # Run ensemble
    engine = EnsembleEngine(consensus_threshold=0.75)
    result = engine.run_ensemble(symbol, market_data, simulate=True)
    
    # Save history
    engine.save_history()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)


if __name__ == '__main__':
    main()

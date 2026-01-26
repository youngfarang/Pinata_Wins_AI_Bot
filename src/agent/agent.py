"""Main AI Agent for Pinata Wins online betting."""

import logging
from typing import Dict, List, Optional
from .strategy import BettingStrategy


class PinataAgent:
    """AI Agent for automated online play and line betting in Pinata Wins."""
    
    def __init__(self, initial_balance: float = 1000.0, strategy: Optional[BettingStrategy] = None):
        """
        Initialize the Pinata AI Agent.
        
        Args:
            initial_balance: Starting bankroll for betting
            strategy: Betting strategy to use (default: conservative)
        """
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.strategy = strategy or BettingStrategy()
        self.bet_history: List[Dict] = []
        self.logger = logging.getLogger(__name__)
        
    def place_line_bet(self, num_lines: int, bet_per_line: float) -> Dict:
        """
        Place a bet on multiple paylines.
        
        Args:
            num_lines: Number of paylines to bet on (1-25)
            bet_per_line: Amount to bet per line
            
        Returns:
            Dictionary with bet details
        """
        total_bet = num_lines * bet_per_line
        
        if total_bet > self.balance:
            self.logger.warning(f"Insufficient balance. Bet: {total_bet}, Balance: {self.balance}")
            return {"success": False, "error": "Insufficient balance"}
        
        bet_info = {
            "num_lines": num_lines,
            "bet_per_line": bet_per_line,
            "total_bet": total_bet,
            "success": True
        }
        
        self.balance -= total_bet
        self.bet_history.append(bet_info)
        self.logger.info(f"Placed line bet: {num_lines} lines @ {bet_per_line} each = {total_bet}")
        
        return bet_info
    
    def decide_bet(self, game_state: Optional[Dict] = None) -> Dict:
        """
        Use strategy to decide next bet parameters.
        
        Args:
            game_state: Current game state information
            
        Returns:
            Dictionary with num_lines and bet_per_line
        """
        return self.strategy.calculate_bet(self.balance, self.bet_history, game_state)
    
    def process_win(self, win_amount: float, win_lines: List[int]) -> None:
        """
        Process a win and update balance.
        
        Args:
            win_amount: Amount won
            win_lines: List of winning line numbers
        """
        self.balance += win_amount
        self.logger.info(f"Win! Amount: {win_amount}, Lines: {win_lines}, New balance: {self.balance}")
        
        if self.bet_history:
            self.bet_history[-1].update({
                "win_amount": win_amount,
                "win_lines": win_lines,
                "result": "win"
            })
    
    def process_loss(self) -> None:
        """Process a loss."""
        self.logger.info(f"Loss. Current balance: {self.balance}")
        
        if self.bet_history:
            self.bet_history[-1].update({
                "win_amount": 0,
                "win_lines": [],
                "result": "loss"
            })
    
    def get_stats(self) -> Dict:
        """
        Get agent statistics.
        
        Returns:
            Dictionary with performance statistics
        """
        total_bets = len(self.bet_history)
        wins = sum(1 for bet in self.bet_history if bet.get("result") == "win")
        total_wagered = sum(bet.get("total_bet", 0) for bet in self.bet_history)
        total_won = sum(bet.get("win_amount", 0) for bet in self.bet_history)
        
        return {
            "total_bets": total_bets,
            "wins": wins,
            "losses": total_bets - wins,
            "win_rate": wins / total_bets if total_bets > 0 else 0,
            "current_balance": self.balance,
            "profit_loss": self.balance - self.initial_balance,
            "total_wagered": total_wagered,
            "total_won": total_won,
            "roi": ((total_won - total_wagered) / total_wagered * 100) if total_wagered > 0 else 0
        }
    
    def reset(self, balance: Optional[float] = None) -> None:
        """
        Reset agent to initial state.
        
        Args:
            balance: New balance (optional, uses initial_balance if not provided)
        """
        self.balance = balance if balance is not None else self.initial_balance
        self.bet_history = []
        self.logger.info(f"Agent reset. Balance: {self.balance}")

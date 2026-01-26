"""Betting strategies for the AI agent."""

from typing import Dict, List, Optional
import random


class BettingStrategy:
    """Base betting strategy for line bets."""
    
    # Strategy configuration constants
    RECENT_RESULTS_WINDOW = 5  # Number of recent bets to analyze for adjustments
    
    def __init__(self, strategy_type: str = "conservative"):
        """
        Initialize betting strategy.
        
        Args:
            strategy_type: Type of strategy (conservative, moderate, aggressive)
        """
        self.strategy_type = strategy_type
        
        # Strategy parameters
        self.strategies = {
            "conservative": {
                "min_lines": 5,
                "max_lines": 10,
                "min_bet": 0.10,
                "max_bet": 1.00,
                "balance_ratio": 0.02  # Bet max 2% of balance
            },
            "moderate": {
                "min_lines": 10,
                "max_lines": 20,
                "min_bet": 0.25,
                "max_bet": 2.50,
                "balance_ratio": 0.05  # Bet max 5% of balance
            },
            "aggressive": {
                "min_lines": 15,
                "max_lines": 25,
                "min_bet": 0.50,
                "max_bet": 5.00,
                "balance_ratio": 0.10  # Bet max 10% of balance
            }
        }
        
        self.params = self.strategies.get(strategy_type, self.strategies["conservative"])
    
    def calculate_bet(self, balance: float, bet_history: List[Dict], 
                     game_state: Optional[Dict] = None) -> Dict:
        """
        Calculate optimal bet based on current situation.
        
        Args:
            balance: Current balance
            bet_history: History of previous bets
            game_state: Current game state
            
        Returns:
            Dictionary with num_lines and bet_per_line
        """
        # Determine max bet based on balance
        max_total_bet = balance * self.params["balance_ratio"]
        
        # Choose number of lines
        num_lines = random.randint(self.params["min_lines"], self.params["max_lines"])
        
        # Calculate bet per line
        bet_per_line = min(
            max_total_bet / num_lines,
            self.params["max_bet"]
        )
        bet_per_line = max(bet_per_line, self.params["min_bet"])
        
        # Round to 2 decimal places
        bet_per_line = round(bet_per_line, 2)
        
        # Adjust based on recent performance
        if len(bet_history) >= self.RECENT_RESULTS_WINDOW:
            recent_results = bet_history[-self.RECENT_RESULTS_WINDOW:]
            recent_wins = sum(1 for bet in recent_results if bet.get("result") == "win")
            
            # If on a losing streak, reduce bet
            if recent_wins == 0:
                bet_per_line *= 0.5
                bet_per_line = max(bet_per_line, self.params["min_bet"])
            # If on a winning streak, slightly increase bet
            elif recent_wins >= 4:
                bet_per_line *= 1.2
                bet_per_line = min(bet_per_line, self.params["max_bet"])
        
        return {
            "num_lines": num_lines,
            "bet_per_line": round(bet_per_line, 2)
        }


class MartingaleStrategy(BettingStrategy):
    """Martingale betting strategy - double bet after loss."""
    
    # Strategy configuration constants
    BASE_BET = 0.50  # Base betting amount
    
    def __init__(self):
        """Initialize Martingale strategy."""
        super().__init__("moderate")
        self.base_bet = self.BASE_BET
    
    def calculate_bet(self, balance: float, bet_history: List[Dict], 
                     game_state: Optional[Dict] = None) -> Dict:
        """Calculate bet using Martingale strategy."""
        num_lines = 10
        bet_per_line = self.base_bet
        
        # Double bet after each loss
        if bet_history and bet_history[-1].get("result") == "loss":
            last_bet = bet_history[-1].get("bet_per_line", self.base_bet)
            bet_per_line = last_bet * 2
        
        # Reset to base after win
        if bet_history and bet_history[-1].get("result") == "win":
            bet_per_line = self.base_bet
        
        # Ensure we don't exceed balance
        max_total_bet = balance * 0.1
        bet_per_line = min(bet_per_line, max_total_bet / num_lines)
        bet_per_line = max(bet_per_line, 0.10)
        
        return {
            "num_lines": num_lines,
            "bet_per_line": round(bet_per_line, 2)
        }


class FibonacciStrategy(BettingStrategy):
    """Fibonacci betting strategy - follow Fibonacci sequence."""
    
    # Strategy configuration constants
    WIN_BACKTRACK_STEPS = 2  # Number of steps to move back in sequence on win
    BASE_BET = 0.25  # Base betting amount
    
    def __init__(self):
        """Initialize Fibonacci strategy."""
        super().__init__("conservative")
        self.base_bet = self.BASE_BET
        self.fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
        self.current_index = 0
    
    def calculate_bet(self, balance: float, bet_history: List[Dict], 
                     game_state: Optional[Dict] = None) -> Dict:
        """Calculate bet using Fibonacci strategy."""
        num_lines = 8
        
        # Move forward in sequence on loss
        if bet_history and bet_history[-1].get("result") == "loss":
            self.current_index = min(self.current_index + 1, len(self.fib_sequence) - 1)
        # Move back on win
        elif bet_history and bet_history[-1].get("result") == "win":
            self.current_index = max(self.current_index - self.WIN_BACKTRACK_STEPS, 0)
        
        bet_per_line = self.base_bet * self.fib_sequence[self.current_index]
        
        # Ensure we don't exceed balance
        max_total_bet = balance * 0.05
        bet_per_line = min(bet_per_line, max_total_bet / num_lines)
        bet_per_line = max(bet_per_line, 0.10)
        
        return {
            "num_lines": num_lines,
            "bet_per_line": round(bet_per_line, 2)
        }

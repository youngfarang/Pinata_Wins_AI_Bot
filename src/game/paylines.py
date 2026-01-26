"""Payline management for line betting."""

from typing import List, Dict, Set
import random


class PaylineManager:
    """Manages paylines for slot-style line betting."""
    
    # Standard 5x3 slot payline patterns (25 paylines)
    PAYLINES = {
        1: [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],  # Middle horizontal
        2: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Top horizontal
        3: [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],  # Bottom horizontal
        4: [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)],  # V shape
        5: [(0, 2), (1, 1), (2, 0), (3, 1), (4, 2)],  # Inverted V
        6: [(0, 1), (1, 0), (2, 0), (3, 0), (4, 1)],  # Top zigzag
        7: [(0, 1), (1, 2), (2, 2), (3, 2), (4, 1)],  # Bottom zigzag
        8: [(0, 0), (1, 0), (2, 1), (3, 2), (4, 2)],  # Ascending diagonal
        9: [(0, 2), (1, 2), (2, 1), (3, 0), (4, 0)],  # Descending diagonal
        10: [(0, 1), (1, 2), (2, 1), (3, 0), (4, 1)], # W shape
        11: [(0, 1), (1, 0), (2, 1), (3, 2), (4, 1)], # M shape
        12: [(0, 0), (1, 1), (2, 1), (3, 1), (4, 0)], # Top plateau
        13: [(0, 2), (1, 1), (2, 1), (3, 1), (4, 2)], # Bottom plateau
        14: [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], # Small W
        15: [(0, 2), (1, 1), (2, 2), (3, 1), (4, 2)], # Small M
        16: [(0, 1), (1, 1), (2, 0), (3, 1), (4, 1)], # Top notch
        17: [(0, 1), (1, 1), (2, 2), (3, 1), (4, 1)], # Bottom notch
        18: [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)], # Zigzag up
        19: [(0, 2), (1, 0), (2, 2), (3, 0), (4, 2)], # Zigzag down
        20: [(0, 0), (1, 0), (2, 1), (3, 0), (4, 0)], # Top dip
        21: [(0, 2), (1, 2), (2, 1), (3, 2), (4, 2)], # Bottom rise
        22: [(0, 1), (1, 2), (2, 0), (3, 2), (4, 1)], # Lightning
        23: [(0, 1), (1, 0), (2, 2), (3, 0), (4, 1)], # Reverse lightning
        24: [(0, 2), (1, 0), (2, 1), (3, 2), (4, 0)], # Cross pattern
        25: [(0, 0), (1, 2), (2, 1), (3, 0), (4, 2)], # Reverse cross
    }
    
    # Symbol values and payout multipliers
    SYMBOLS = {
        "PINATA": {"value": 10, "min_match": 2},
        "CANDY": {"value": 5, "min_match": 3},
        "STAR": {"value": 4, "min_match": 3},
        "HEART": {"value": 3, "min_match": 3},
        "DIAMOND": {"value": 2, "min_match": 4},
        "CHERRY": {"value": 1, "min_match": 4},
    }
    
    # Payout multipliers based on number of matching symbols
    PAYOUT_MULTIPLIERS = {
        2: 2,    # 2 symbols in a row
        3: 5,    # 3 symbols in a row
        4: 15,   # 4 symbols in a row
        5: 50,   # 5 symbols in a row (full line)
    }
    
    def __init__(self):
        """Initialize payline manager."""
        self.active_lines: Set[int] = set()
    
    def activate_lines(self, num_lines: int) -> None:
        """
        Activate a number of paylines.
        
        Args:
            num_lines: Number of lines to activate (1-25)
        """
        if num_lines < 1 or num_lines > 25:
            raise ValueError("Number of lines must be between 1 and 25")
        
        self.active_lines = set(range(1, num_lines + 1))
    
    def check_wins(self, reel_grid: List[List[str]], bet_per_line: float) -> Dict:
        """
        Check for winning combinations on active paylines.
        
        Args:
            reel_grid: 5x3 grid of symbols (5 reels, 3 rows)
            bet_per_line: Bet amount per line
            
        Returns:
            Dictionary with win details
        """
        winning_lines = []
        total_win = 0.0
        
        for line_num in self.active_lines:
            payline = self.PAYLINES[line_num]
            symbols = [reel_grid[col][row] for col, row in payline]
            
            # Check for matching symbols from left to right
            match_count = 1
            first_symbol = symbols[0]
            
            for i in range(1, len(symbols)):
                if symbols[i] == first_symbol:
                    match_count += 1
                else:
                    break
            
            # Check if we have a winning combination
            symbol_info = self.SYMBOLS.get(first_symbol, {"value": 1, "min_match": 5})
            if match_count >= symbol_info["min_match"]:
                multiplier = self.PAYOUT_MULTIPLIERS.get(match_count, 1)
                symbol_value = symbol_info["value"]
                line_win = bet_per_line * multiplier * symbol_value
                
                winning_lines.append({
                    "line": line_num,
                    "symbol": first_symbol,
                    "count": match_count,
                    "win_amount": line_win
                })
                
                total_win += line_win
        
        return {
            "winning_lines": winning_lines,
            "total_win": round(total_win, 2),
            "num_wins": len(winning_lines)
        }
    
    def generate_random_spin(self) -> List[List[str]]:
        """
        Generate a random spin result (5x3 grid).
        
        Returns:
            5x3 grid of symbols
        """
        # Weight symbols for realistic probabilities
        symbol_weights = {
            "PINATA": 5,
            "CANDY": 10,
            "STAR": 15,
            "HEART": 20,
            "DIAMOND": 25,
            "CHERRY": 25,
        }
        
        symbols = []
        weights = []
        for symbol, weight in symbol_weights.items():
            symbols.append(symbol)
            weights.append(weight)
        
        # Generate 5 reels with 3 symbols each
        reel_grid = []
        for _ in range(5):
            reel = random.choices(symbols, weights=weights, k=3)
            reel_grid.append(reel)
        
        return reel_grid
    
    def get_payline_pattern(self, line_num: int) -> List[tuple]:
        """
        Get the pattern for a specific payline.
        
        Args:
            line_num: Payline number (1-25)
            
        Returns:
            List of (column, row) tuples
        """
        return self.PAYLINES.get(line_num, [])

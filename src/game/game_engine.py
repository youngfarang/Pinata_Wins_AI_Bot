"""Game engine for Pinata Wins simulation."""

import logging
from typing import Dict, List, Optional
from .paylines import PaylineManager


class GameEngine:
    """Simulates Pinata Wins game mechanics."""
    
    def __init__(self):
        """Initialize game engine."""
        self.payline_manager = PaylineManager()
        self.logger = logging.getLogger(__name__)
        self.spin_count = 0
        self.total_wagered = 0.0
        self.total_paid = 0.0
    
    def spin(self, num_lines: int, bet_per_line: float) -> Dict:
        """
        Execute a spin with line bets.
        
        Args:
            num_lines: Number of active paylines
            bet_per_line: Bet amount per line
            
        Returns:
            Dictionary with spin results
        """
        self.spin_count += 1
        total_bet = num_lines * bet_per_line
        self.total_wagered += total_bet
        
        # Activate paylines
        self.payline_manager.activate_lines(num_lines)
        
        # Generate random spin result
        reel_grid = self.payline_manager.generate_random_spin()
        
        # Check for wins
        win_result = self.payline_manager.check_wins(reel_grid, bet_per_line)
        
        self.total_paid += win_result["total_win"]
        
        result = {
            "spin_number": self.spin_count,
            "reel_grid": reel_grid,
            "num_lines": num_lines,
            "bet_per_line": bet_per_line,
            "total_bet": total_bet,
            "winning_lines": win_result["winning_lines"],
            "total_win": win_result["total_win"],
            "num_wins": win_result["num_wins"],
            "profit": win_result["total_win"] - total_bet
        }
        
        self.logger.info(f"Spin #{self.spin_count}: Bet {total_bet}, Win {win_result['total_win']}, "
                        f"Lines: {win_result['num_wins']}")
        
        return result
    
    def display_grid(self, reel_grid: List[List[str]]) -> str:
        """
        Display the reel grid in a readable format.
        
        Args:
            reel_grid: 5x3 grid of symbols
            
        Returns:
            Formatted string representation
        """
        rows = []
        for row_idx in range(3):
            row = []
            for col_idx in range(5):
                symbol = reel_grid[col_idx][row_idx]
                row.append(f"{symbol:^10}")
            rows.append(" | ".join(row))
        
        separator = "-" * 58
        grid_str = f"\n{separator}\n" + f"\n{separator}\n".join(rows) + f"\n{separator}\n"
        return grid_str
    
    def get_rtp(self) -> float:
        """
        Calculate Return to Player (RTP) percentage.
        
        Returns:
            RTP as a percentage
        """
        if self.total_wagered == 0:
            return 0.0
        return (self.total_paid / self.total_wagered) * 100
    
    def get_stats(self) -> Dict:
        """
        Get game statistics.
        
        Returns:
            Dictionary with game stats
        """
        return {
            "total_spins": self.spin_count,
            "total_wagered": round(self.total_wagered, 2),
            "total_paid": round(self.total_paid, 2),
            "net_result": round(self.total_paid - self.total_wagered, 2),
            "rtp": round(self.get_rtp(), 2)
        }
    
    def reset(self) -> None:
        """Reset game statistics."""
        self.spin_count = 0
        self.total_wagered = 0.0
        self.total_paid = 0.0
        self.logger.info("Game engine reset")

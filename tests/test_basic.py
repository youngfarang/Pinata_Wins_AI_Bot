"""
Unit tests for Pinata Wins AI Bot.

Run with: python -m pytest tests/ -v
Or: python tests/test_basic.py
"""

import unittest
from src.agent import PinataAgent
from src.agent.strategy import BettingStrategy
from src.game import GameEngine, PaylineManager
from src.client import GameClient


class TestPinataAgent(unittest.TestCase):
    """Test cases for PinataAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = PinataAgent(initial_balance=1000.0)
    
    def test_initial_balance(self):
        """Test agent initialization with correct balance."""
        self.assertEqual(self.agent.balance, 1000.0)
        self.assertEqual(self.agent.initial_balance, 1000.0)
    
    def test_place_line_bet_success(self):
        """Test successful line bet placement."""
        result = self.agent.place_line_bet(10, 1.0)
        self.assertTrue(result["success"])
        self.assertEqual(result["total_bet"], 10.0)
        self.assertEqual(self.agent.balance, 990.0)
    
    def test_place_line_bet_insufficient_balance(self):
        """Test bet placement with insufficient balance."""
        result = self.agent.place_line_bet(25, 100.0)  # 2500 total
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertEqual(self.agent.balance, 1000.0)  # Balance unchanged
    
    def test_process_win(self):
        """Test win processing."""
        self.agent.place_line_bet(10, 1.0)
        initial = self.agent.balance
        self.agent.process_win(50.0, [1, 2, 3])
        self.assertEqual(self.agent.balance, initial + 50.0)
    
    def test_process_loss(self):
        """Test loss processing."""
        self.agent.place_line_bet(10, 1.0)
        balance_after_bet = self.agent.balance
        self.agent.process_loss()
        self.assertEqual(self.agent.balance, balance_after_bet)
    
    def test_get_stats(self):
        """Test statistics retrieval."""
        self.agent.place_line_bet(5, 1.0)
        self.agent.process_win(10.0, [1])
        stats = self.agent.get_stats()
        
        self.assertEqual(stats["total_bets"], 1)
        self.assertEqual(stats["wins"], 1)
        self.assertEqual(stats["losses"], 0)
        self.assertEqual(stats["win_rate"], 1.0)
    
    def test_reset(self):
        """Test agent reset."""
        self.agent.place_line_bet(10, 1.0)
        self.agent.reset()
        self.assertEqual(self.agent.balance, 1000.0)
        self.assertEqual(len(self.agent.bet_history), 0)


class TestBettingStrategy(unittest.TestCase):
    """Test cases for BettingStrategy class."""
    
    def test_conservative_strategy(self):
        """Test conservative strategy parameters."""
        strategy = BettingStrategy("conservative")
        bet = strategy.calculate_bet(1000.0, [], None)
        
        self.assertIn("num_lines", bet)
        self.assertIn("bet_per_line", bet)
        self.assertGreaterEqual(bet["num_lines"], 5)
        self.assertLessEqual(bet["num_lines"], 10)
    
    def test_moderate_strategy(self):
        """Test moderate strategy parameters."""
        strategy = BettingStrategy("moderate")
        bet = strategy.calculate_bet(1000.0, [], None)
        
        self.assertGreaterEqual(bet["num_lines"], 10)
        self.assertLessEqual(bet["num_lines"], 20)
    
    def test_aggressive_strategy(self):
        """Test aggressive strategy parameters."""
        strategy = BettingStrategy("aggressive")
        bet = strategy.calculate_bet(1000.0, [], None)
        
        self.assertGreaterEqual(bet["num_lines"], 15)
        self.assertLessEqual(bet["num_lines"], 25)


class TestPaylineManager(unittest.TestCase):
    """Test cases for PaylineManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = PaylineManager()
    
    def test_activate_lines(self):
        """Test payline activation."""
        self.manager.activate_lines(10)
        self.assertEqual(len(self.manager.active_lines), 10)
    
    def test_activate_lines_invalid(self):
        """Test invalid payline activation."""
        with self.assertRaises(ValueError):
            self.manager.activate_lines(0)
        with self.assertRaises(ValueError):
            self.manager.activate_lines(26)
    
    def test_generate_random_spin(self):
        """Test random spin generation."""
        grid = self.manager.generate_random_spin()
        
        # Check grid dimensions: 5 reels x 3 rows
        self.assertEqual(len(grid), 5)
        for reel in grid:
            self.assertEqual(len(reel), 3)
    
    def test_check_wins_no_active_lines(self):
        """Test win checking with no active lines."""
        grid = self.manager.generate_random_spin()
        result = self.manager.check_wins(grid, 1.0)
        
        self.assertEqual(result["total_win"], 0)
        self.assertEqual(result["num_wins"], 0)
    
    def test_get_payline_pattern(self):
        """Test payline pattern retrieval."""
        pattern = self.manager.get_payline_pattern(1)
        self.assertEqual(len(pattern), 5)  # 5 positions in a payline


class TestGameEngine(unittest.TestCase):
    """Test cases for GameEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
    
    def test_spin(self):
        """Test game spin execution."""
        result = self.engine.spin(10, 1.0)
        
        self.assertIn("spin_number", result)
        self.assertIn("reel_grid", result)
        self.assertIn("total_bet", result)
        self.assertIn("total_win", result)
        self.assertEqual(result["total_bet"], 10.0)
        self.assertEqual(result["spin_number"], 1)
    
    def test_get_stats(self):
        """Test game statistics."""
        self.engine.spin(10, 1.0)
        stats = self.engine.get_stats()
        
        self.assertEqual(stats["total_spins"], 1)
        self.assertEqual(stats["total_wagered"], 10.0)
    
    def test_reset(self):
        """Test game engine reset."""
        self.engine.spin(10, 1.0)
        self.engine.reset()
        
        stats = self.engine.get_stats()
        self.assertEqual(stats["total_spins"], 0)
        self.assertEqual(stats["total_wagered"], 0.0)


class TestGameClient(unittest.TestCase):
    """Test cases for GameClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = PinataAgent(initial_balance=500.0)
        self.client = GameClient(self.agent)
    
    def test_play_single_round(self):
        """Test single round play."""
        result = self.client.play_single_round(online=False)
        
        self.assertTrue(result["success"])
        self.assertIn("spin_result", result)
        self.assertIn("agent_balance", result)
    
    def test_auto_play(self):
        """Test auto-play session."""
        result = self.client.start_auto_play(max_spins=5, online=False)
        
        self.assertEqual(result["spins_completed"], 5)
        self.assertIn("agent_stats", result)
        self.assertIn("game_stats", result)
    
    def test_stop_loss(self):
        """Test stop loss condition."""
        result = self.client.start_auto_play(
            max_spins=100,
            stop_loss=400.0,
            online=False
        )
        
        # Should stop before 100 spins if balance drops
        self.assertLessEqual(result["final_balance"], 500.0)
    
    def test_get_status(self):
        """Test client status retrieval."""
        status = self.client.get_status()
        
        self.assertIn("connected", status)
        self.assertIn("agent_balance", status)
        self.assertIn("auto_play_active", status)


if __name__ == "__main__":
    unittest.main()

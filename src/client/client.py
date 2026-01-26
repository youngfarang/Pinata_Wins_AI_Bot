"""Game client for online play."""

import logging
from typing import Optional, Dict
from .connection import ConnectionManager
from ..agent import PinataAgent
from ..game import GameEngine


class GameClient:
    """Client for playing Pinata Wins online with AI agent."""
    
    def __init__(self, agent: PinataAgent, server_url: Optional[str] = None):
        """
        Initialize game client.
        
        Args:
            agent: AI agent for automated play
            server_url: Server URL for online play
        """
        self.agent = agent
        self.connection = ConnectionManager(server_url)
        self.game_engine = GameEngine()
        self.logger = logging.getLogger(__name__)
        self.auto_play = False
        self.max_spins: Optional[int] = None
        self.stop_loss: Optional[float] = None
        self.stop_win: Optional[float] = None
    
    def connect(self, auth_token: Optional[str] = None) -> bool:
        """
        Connect to online game server.
        
        Args:
            auth_token: Authentication token
            
        Returns:
            True if connection successful
        """
        return self.connection.connect(auth_token)
    
    def disconnect(self) -> None:
        """Disconnect from server."""
        self.connection.disconnect()
    
    def play_single_round(self, online: bool = False) -> Dict:
        """
        Play a single round.
        
        Args:
            online: If True, play online; if False, play locally
            
        Returns:
            Dictionary with round results
        """
        # Agent decides bet
        bet_decision = self.agent.decide_bet()
        num_lines = bet_decision["num_lines"]
        bet_per_line = bet_decision["bet_per_line"]
        
        # Place bet
        bet_result = self.agent.place_line_bet(num_lines, bet_per_line)
        
        if not bet_result["success"]:
            return {
                "success": False,
                "error": bet_result.get("error", "Bet failed")
            }
        
        # Execute spin
        if online and self.connection.is_connected():
            # Send bet to server
            self.connection.send_message("spin", {
                "num_lines": num_lines,
                "bet_per_line": bet_per_line
            })
            
            # Receive result from server
            spin_result = self.connection.receive_message()
            
            # For now, fallback to local simulation if no server response
            if not spin_result:
                spin_result = self.game_engine.spin(num_lines, bet_per_line)
        else:
            # Play locally
            spin_result = self.game_engine.spin(num_lines, bet_per_line)
        
        # Process result
        if spin_result["total_win"] > 0:
            self.agent.process_win(
                spin_result["total_win"],
                [line["line"] for line in spin_result["winning_lines"]]
            )
        else:
            self.agent.process_loss()
        
        return {
            "success": True,
            "spin_result": spin_result,
            "agent_balance": self.agent.balance
        }
    
    def start_auto_play(self, max_spins: Optional[int] = None, 
                       stop_loss: Optional[float] = None,
                       stop_win: Optional[float] = None,
                       online: bool = False) -> Dict:
        """
        Start automated play session.
        
        Args:
            max_spins: Maximum number of spins (None for unlimited)
            stop_loss: Stop if balance drops below this amount
            stop_win: Stop if balance reaches this amount
            online: If True, play online; if False, play locally
            
        Returns:
            Dictionary with session results
        """
        self.auto_play = True
        self.max_spins = max_spins
        self.stop_loss = stop_loss
        self.stop_win = stop_win
        
        self.logger.info(f"Starting auto-play session (max_spins={max_spins}, "
                        f"stop_loss={stop_loss}, stop_win={stop_win})")
        
        spins_completed = 0
        initial_balance = self.agent.balance
        
        try:
            while self.auto_play:
                # Check stopping conditions
                if max_spins and spins_completed >= max_spins:
                    self.logger.info(f"Reached max spins: {max_spins}")
                    break
                
                if stop_loss and self.agent.balance <= stop_loss:
                    self.logger.info(f"Stop loss triggered: {self.agent.balance} <= {stop_loss}")
                    break
                
                if stop_win and self.agent.balance >= stop_win:
                    self.logger.info(f"Stop win triggered: {self.agent.balance} >= {stop_win}")
                    break
                
                # Play round
                round_result = self.play_single_round(online=online)
                
                if not round_result["success"]:
                    self.logger.warning(f"Round failed: {round_result.get('error')}")
                    break
                
                spins_completed += 1
                
        except KeyboardInterrupt:
            self.logger.info("Auto-play interrupted by user")
        
        self.auto_play = False
        
        # Compile session results
        agent_stats = self.agent.get_stats()
        game_stats = self.game_engine.get_stats()
        
        return {
            "spins_completed": spins_completed,
            "initial_balance": initial_balance,
            "final_balance": self.agent.balance,
            "profit_loss": self.agent.balance - initial_balance,
            "agent_stats": agent_stats,
            "game_stats": game_stats
        }
    
    def stop_auto_play(self) -> None:
        """Stop automated play."""
        self.auto_play = False
        self.logger.info("Stopping auto-play")
    
    def get_status(self) -> Dict:
        """
        Get current client status.
        
        Returns:
            Dictionary with status information
        """
        return {
            "connected": self.connection.is_connected(),
            "session_info": self.connection.get_session_info(),
            "agent_balance": self.agent.balance,
            "agent_stats": self.agent.get_stats(),
            "game_stats": self.game_engine.get_stats(),
            "auto_play_active": self.auto_play
        }

"""Main entry point for Pinata Wins AI Bot."""

import logging
import argparse
from src.agent import PinataAgent
from src.agent.strategy import BettingStrategy, MartingaleStrategy, FibonacciStrategy
from src.client import GameClient


def setup_logging(level: str = "INFO") -> None:
    """
    Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    """Main function to run the Pinata Wins AI Bot."""
    parser = argparse.ArgumentParser(description='Pinata Wins AI Bot - Automated Online Play with Line Betting')
    
    parser.add_argument('--balance', type=float, default=1000.0,
                       help='Initial balance (default: 1000.0)')
    parser.add_argument('--strategy', type=str, default='conservative',
                       choices=['conservative', 'moderate', 'aggressive', 'martingale', 'fibonacci'],
                       help='Betting strategy to use (default: conservative)')
    parser.add_argument('--max-spins', type=int, default=None,
                       help='Maximum number of spins (default: unlimited)')
    parser.add_argument('--stop-loss', type=float, default=None,
                       help='Stop if balance drops below this amount')
    parser.add_argument('--stop-win', type=float, default=None,
                       help='Stop if balance reaches this amount')
    parser.add_argument('--online', action='store_true',
                       help='Play online (requires server connection)')
    parser.add_argument('--server-url', type=str, default=None,
                       help='Server URL for online play')
    parser.add_argument('--log-level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    parser.add_argument('--single', action='store_true',
                       help='Play a single round instead of auto-play')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Create betting strategy
    if args.strategy == 'martingale':
        strategy = MartingaleStrategy()
    elif args.strategy == 'fibonacci':
        strategy = FibonacciStrategy()
    else:
        strategy = BettingStrategy(args.strategy)
    
    # Create agent
    logger.info(f"Creating AI agent with {args.strategy} strategy and balance ${args.balance}")
    agent = PinataAgent(initial_balance=args.balance, strategy=strategy)
    
    # Create client
    client = GameClient(agent, server_url=args.server_url)
    
    # Connect if online mode
    if args.online:
        logger.info("Connecting to online server...")
        if not client.connect():
            logger.error("Failed to connect to server. Running in offline mode.")
            args.online = False
    
    try:
        if args.single:
            # Play single round
            logger.info("Playing single round...")
            result = client.play_single_round(online=args.online)
            
            if result["success"]:
                spin = result["spin_result"]
                logger.info(f"\n{'='*60}")
                logger.info(f"SPIN RESULT - Spin #{spin['spin_number']}")
                logger.info(f"{'='*60}")
                logger.info(client.game_engine.display_grid(spin['reel_grid']))
                logger.info(f"Bet: {spin['num_lines']} lines @ ${spin['bet_per_line']} = ${spin['total_bet']}")
                logger.info(f"Win: ${spin['total_win']} on {spin['num_wins']} line(s)")
                logger.info(f"Profit: ${spin['profit']:.2f}")
                logger.info(f"Balance: ${result['agent_balance']:.2f}")
            else:
                logger.error(f"Round failed: {result.get('error')}")
        else:
            # Start auto-play
            logger.info("Starting auto-play session...")
            session_result = client.start_auto_play(
                max_spins=args.max_spins,
                stop_loss=args.stop_loss,
                stop_win=args.stop_win,
                online=args.online
            )
            
            # Display session summary
            logger.info(f"\n{'='*60}")
            logger.info(f"AUTO-PLAY SESSION SUMMARY")
            logger.info(f"{'='*60}")
            logger.info(f"Spins Completed: {session_result['spins_completed']}")
            logger.info(f"Initial Balance: ${session_result['initial_balance']:.2f}")
            logger.info(f"Final Balance: ${session_result['final_balance']:.2f}")
            logger.info(f"Profit/Loss: ${session_result['profit_loss']:.2f}")
            logger.info(f"\nAgent Statistics:")
            for key, value in session_result['agent_stats'].items():
                logger.info(f"  {key}: {value}")
            logger.info(f"\nGame Statistics:")
            for key, value in session_result['game_stats'].items():
                logger.info(f"  {key}: {value}")
            logger.info(f"{'='*60}")
    
    finally:
        # Cleanup
        if args.online:
            client.disconnect()
        logger.info("Session ended.")


if __name__ == "__main__":
    main()

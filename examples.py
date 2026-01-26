#!/usr/bin/env python3
"""
Example demonstration script for Pinata Wins AI Bot.

This script demonstrates various features of the bot including:
- Different betting strategies
- Single round and auto-play modes
- Stop conditions
- Statistics tracking
"""

import logging
from src.agent import PinataAgent
from src.agent.strategy import BettingStrategy, MartingaleStrategy, FibonacciStrategy
from src.client import GameClient
from src.game import GameEngine


def setup_logging():
    """Setup basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


def demo_single_round():
    """Demonstrate single round play."""
    print("\n" + "="*60)
    print("DEMO 1: Single Round Play")
    print("="*60)
    
    agent = PinataAgent(initial_balance=100.0, strategy=BettingStrategy("conservative"))
    client = GameClient(agent)
    
    result = client.play_single_round(online=False)
    
    if result["success"]:
        spin = result["spin_result"]
        print(f"\nReel Grid:")
        print(client.game_engine.display_grid(spin['reel_grid']))
        print(f"Bet: {spin['num_lines']} lines @ ${spin['bet_per_line']} = ${spin['total_bet']}")
        print(f"Win: ${spin['total_win']} on {spin['num_wins']} line(s)")
        print(f"Balance: ${result['agent_balance']:.2f}")


def demo_auto_play():
    """Demonstrate auto-play with stop conditions."""
    print("\n" + "="*60)
    print("DEMO 2: Auto-Play with Stop Conditions")
    print("="*60)
    
    agent = PinataAgent(initial_balance=200.0, strategy=BettingStrategy("moderate"))
    client = GameClient(agent)
    
    print("\nStarting auto-play: 20 spins or stop at $300 win...")
    result = client.start_auto_play(
        max_spins=20,
        stop_loss=100.0,
        stop_win=300.0,
        online=False
    )
    
    print(f"\nSession Summary:")
    print(f"  Spins: {result['spins_completed']}")
    print(f"  Initial: ${result['initial_balance']:.2f}")
    print(f"  Final: ${result['final_balance']:.2f}")
    print(f"  Profit/Loss: ${result['profit_loss']:.2f}")
    print(f"  Win Rate: {result['agent_stats']['win_rate']:.1%}")
    print(f"  ROI: {result['agent_stats']['roi']:.2f}%")


def demo_strategies():
    """Compare different betting strategies."""
    print("\n" + "="*60)
    print("DEMO 3: Strategy Comparison")
    print("="*60)
    
    strategies = [
        ("Conservative", BettingStrategy("conservative")),
        ("Moderate", BettingStrategy("moderate")),
        ("Aggressive", BettingStrategy("aggressive")),
        ("Martingale", MartingaleStrategy()),
        ("Fibonacci", FibonacciStrategy())
    ]
    
    print(f"\nRunning 10 spins with each strategy (starting balance: $100)...\n")
    
    results = []
    for name, strategy in strategies:
        agent = PinataAgent(initial_balance=100.0, strategy=strategy)
        client = GameClient(agent)
        
        session = client.start_auto_play(max_spins=10, online=False)
        results.append({
            "name": name,
            "final_balance": session['final_balance'],
            "profit_loss": session['profit_loss'],
            "win_rate": session['agent_stats']['win_rate'],
            "roi": session['agent_stats']['roi']
        })
    
    print(f"{'Strategy':<15} {'Final Balance':<15} {'Profit/Loss':<15} {'Win Rate':<12} {'ROI':<10}")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<15} ${r['final_balance']:<14.2f} ${r['profit_loss']:<14.2f} "
              f"{r['win_rate']:<11.1%} {r['roi']:<9.2f}%")


def demo_paylines():
    """Demonstrate payline mechanics."""
    print("\n" + "="*60)
    print("DEMO 4: Payline Mechanics")
    print("="*60)
    
    from src.game.paylines import PaylineManager
    
    manager = PaylineManager()
    
    print("\nShowing first 5 payline patterns:")
    for i in range(1, 6):
        pattern = manager.get_payline_pattern(i)
        print(f"\nPayline {i}: {pattern}")
        
    print("\n\nSymbol payout information:")
    print(f"{'Symbol':<10} {'Value':<8} {'Min Match':<12}")
    print("-" * 30)
    for symbol, info in manager.SYMBOLS.items():
        print(f"{symbol:<10} {info['value']}x       {info['min_match']}")
    
    print("\n\nPayout multipliers:")
    for count, mult in manager.PAYOUT_MULTIPLIERS.items():
        print(f"  {count} symbols in a row: {mult}x")


def demo_statistics():
    """Demonstrate comprehensive statistics tracking."""
    print("\n" + "="*60)
    print("DEMO 5: Statistics Tracking")
    print("="*60)
    
    agent = PinataAgent(initial_balance=500.0, strategy=BettingStrategy("moderate"))
    client = GameClient(agent)
    
    print("\nRunning 50 spins to gather statistics...")
    session = client.start_auto_play(max_spins=50, online=False)
    
    print(f"\nAgent Statistics:")
    stats = session['agent_stats']
    print(f"  Total Bets: {stats['total_bets']}")
    print(f"  Wins: {stats['wins']}")
    print(f"  Losses: {stats['losses']}")
    print(f"  Win Rate: {stats['win_rate']:.1%}")
    print(f"  Total Wagered: ${stats['total_wagered']:.2f}")
    print(f"  Total Won: ${stats['total_won']:.2f}")
    print(f"  ROI: {stats['roi']:.2f}%")
    print(f"  Final Balance: ${stats['current_balance']:.2f}")
    print(f"  Profit/Loss: ${stats['profit_loss']:.2f}")
    
    print(f"\nGame Statistics:")
    game_stats = session['game_stats']
    print(f"  Total Spins: {game_stats['total_spins']}")
    print(f"  RTP (Return to Player): {game_stats['rtp']:.2f}%")


def main():
    """Run all demonstrations."""
    setup_logging()
    
    print("\n" + "="*60)
    print("PINATA WINS AI BOT - FEATURE DEMONSTRATIONS")
    print("="*60)
    
    demos = [
        ("Single Round Play", demo_single_round),
        ("Auto-Play Mode", demo_auto_play),
        ("Strategy Comparison", demo_strategies),
        ("Payline Mechanics", demo_paylines),
        ("Statistics Tracking", demo_statistics)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            demo_func()
        except Exception as e:
            print(f"\nError in {name}: {e}")
        
        if i < len(demos):
            input("\nPress Enter to continue to next demo...")
    
    print("\n" + "="*60)
    print("DEMONSTRATIONS COMPLETE")
    print("="*60)
    print("\nFor more information, run: python main.py --help")


if __name__ == "__main__":
    main()

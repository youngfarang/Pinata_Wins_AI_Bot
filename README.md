# Pinata Wins AI Bot

An AI-powered bot for automated online play with line betting in the Pinata Wins slot game.

## Features

- **AI Agent**: Intelligent betting decisions using multiple strategies
- **Line Betting**: Support for 1-25 paylines with configurable bet amounts
- **Online Play**: Connect to game servers for real-time play
- **Multiple Strategies**: Conservative, Moderate, Aggressive, Martingale, and Fibonacci betting strategies
- **Auto-Play**: Automated gameplay with configurable stopping conditions
- **Statistics Tracking**: Comprehensive tracking of bets, wins, losses, and ROI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/youngfarang/Pinata_Wins_AI_Bot.git
cd Pinata_Wins_AI_Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Local Simulation)

Play a single round:
```bash
python main.py --single
```

Auto-play with default settings:
```bash
python main.py
```

### Advanced Options

**Choose betting strategy:**
```bash
python main.py --strategy aggressive --balance 2000
```

**Set stopping conditions:**
```bash
python main.py --max-spins 50 --stop-loss 500 --stop-win 1500
```

**Online play (requires server):**
```bash
python main.py --online --server-url ws://game.server:8080
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--balance` | Initial balance | 1000.0 |
| `--strategy` | Betting strategy (conservative/moderate/aggressive/martingale/fibonacci) | conservative |
| `--max-spins` | Maximum number of spins | Unlimited |
| `--stop-loss` | Stop if balance drops below this | None |
| `--stop-win` | Stop if balance reaches this | None |
| `--online` | Enable online play | False |
| `--server-url` | Server URL for online play | ws://localhost:8080 |
| `--log-level` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO |
| `--single` | Play single round instead of auto-play | False |

## Betting Strategies

### Conservative
- Bets on 5-10 paylines
- Minimum bet: $0.10, Maximum bet: $1.00
- Uses 2% of balance per bet
- Reduces bet on losing streaks

### Moderate
- Bets on 10-20 paylines
- Minimum bet: $0.25, Maximum bet: $2.50
- Uses 5% of balance per bet
- Balanced risk/reward

### Aggressive
- Bets on 15-25 paylines
- Minimum bet: $0.50, Maximum bet: $5.00
- Uses 10% of balance per bet
- Higher risk, higher potential reward

### Martingale
- Doubles bet after each loss
- Resets to base bet after win
- High risk strategy

### Fibonacci
- Follows Fibonacci sequence for bet progression
- Moves forward on loss, back on win
- Moderate risk strategy

## Project Structure

```
Pinata_Wins_AI_Bot/
├── src/
│   ├── agent/              # AI agent logic
│   │   ├── agent.py        # Main agent class
│   │   └── strategy.py     # Betting strategies
│   ├── game/               # Game mechanics
│   │   ├── game_engine.py  # Game simulation
│   │   └── paylines.py     # Payline management
│   └── client/             # Online play client
│       ├── client.py       # Game client
│       └── connection.py   # Server connection
├── config/                 # Configuration files
├── tests/                  # Unit tests
├── main.py                 # Entry point
└── requirements.txt        # Python dependencies
```

## Game Mechanics

### Symbols and Payouts

| Symbol | Value | Min Match |
|--------|-------|-----------|
| PINATA | 10x | 2 |
| CANDY | 5x | 3 |
| STAR | 4x | 3 |
| HEART | 3x | 3 |
| DIAMOND | 2x | 4 |
| CHERRY | 1x | 4 |

### Payout Multipliers

- 2 matching symbols: 2x
- 3 matching symbols: 5x
- 4 matching symbols: 15x
- 5 matching symbols: 50x

## Examples

**Example 1: Quick test with 10 spins**
```bash
python main.py --max-spins 10 --balance 500
```

**Example 2: Aggressive strategy with stop conditions**
```bash
python main.py --strategy aggressive --balance 1000 --stop-loss 500 --stop-win 2000
```

**Example 3: Martingale strategy with verbose logging**
```bash
python main.py --strategy martingale --log-level DEBUG --max-spins 20
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This bot is for educational and entertainment purposes only. Always gamble responsibly and within your means.
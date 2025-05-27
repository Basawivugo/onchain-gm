# Multi-Chain GM Sender

This application allows you to send "GM" transactions on multiple blockchain networks from multiple wallets through an interactive menu system.

## Features

- Interactive menu system for easy use
- Support for multiple blockchains with dynamic chain selection
- **Chain configuration via .env file** - specify which chain to use
- **Configurable random delays between wallet processing** - set min/max range
- **Wallet shuffling functionality** for randomized processing order
- Multiple wallet management from a simple text file
- Organized directory structure
- Transaction status tracking and summaries

## Current Supported Chains

- MegaETH (Chain ID: 6342)
- Unichain (Chain ID: 130)
- Soneium (Chain ID: 1868)
- Inkchain (Chain ID: 57073)
- Monad (Chain ID: 41454)

## Project Structure

```
├── chains/                  # Chain implementations
│   ├── __init__.py          # Chain registry
│   ├── megaETH.py           # MegaETH chain implementation
│   ├── unichain.py          # Unichain chain implementation
│   ├── soneium.py           # Soneium chain implementation
│   ├── inkchain.py          # Inkchain chain implementation
│   └── monad.py             # Monad chain implementation
├── data/                    # Data storage
│   ├── private_keys.txt     # Private keys (one per line)
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── menu.py              # Menu system
│   ├── version_checker.py   # Version Manager
│   └── wallet_manager.py    # Wallet management functions
├── .env                     # Configuration (RPC URLs, chain selection, delays)
├── .gitignore               # Git ignore list
├── main.py                  # Main application with menu
└── requirements.txt         # Python dependencies
```

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Rename env.example to .env
4. Run the application:
   ```
   python main.py or python3 main.py
   ```
5. The application will create `data/private_keys.txt` if it doesn't exist
6. Edit `data/private_keys.txt` to add your private keys (one per line)

## Configuration

The application uses a `.env` file for configuration. Here are the available options:

### RPC URLs
```env
MEGAETH_RPC_URL=https://carrot.megaeth.com/rpc 
UNICHAIN_RPC_URL=https://unichain.drpc.org
SONEIUM_RPC_URL=https://soneium.drpc.org
INKCHAIN_RPC_URL=https://ink.drpc.org
MONAD_RPC_URL=https://testnet-rpc.monad.xyz
```

### Chain Selection
```env
# Specify which chain to use: megaeth, unichain, soneium, inkchain, monad, or "all" for all chains
CHAIN=unichain
```

### Timing Configuration
```env
# Random delay between processing wallets (in seconds)
# The application will use a random delay between min and max values
MIN_DELAY_BETWEEN_WALLETS=1
MAX_DELAY_BETWEEN_WALLETS=3

# For fixed delay, set both values to the same number
MIN_DELAY_BETWEEN_WALLETS=2
MAX_DELAY_BETWEEN_WALLETS=2
```

### Wallet Processing Options
```env
# Set to true to shuffle wallets before processing
SHUFFLE_WALLETS=false
```

## Private Keys File Format

The application reads private keys from `data/private_keys.txt`. The format is simple:

- One private key per line
- Lines starting with `#` are treated as comments and ignored
- Private keys can include or omit the `0x` prefix

Example:

```
0x1111111111111111111111111111111111111111111111111111111111111111
0x2222222222222222222222222222222222222222222222222222222222222222
3333333333333333333333333333333333333333333333333333333333333333
```
Keys without 0x prefix also work

## Using the Menu System

The application provides a simple menu with the following options:

1. **Send GM (using .env configuration)**: Send GM using the chain specified in your .env file
2. **Exit**: Exit the application

## Configuration Features

### Chain Selection
You can specify which chain to use in the `.env` file:
- Set `CHAIN=unichain` to use only Unichain
- Set `CHAIN=megaeth` to use only MegaETH
- Set `CHAIN=all` to use all available chains
- Any supported chain name works

### Random Delay Between Wallets
Configure random delays between processing wallets to avoid rate limiting and appear more human-like:
- Set `MIN_DELAY_BETWEEN_WALLETS=1` and `MAX_DELAY_BETWEEN_WALLETS=5` for 1-5 second random delays
- Set `MIN_DELAY_BETWEEN_WALLETS=0.5` and `MAX_DELAY_BETWEEN_WALLETS=2.5` for 0.5-2.5 second random delays
- Set both values to the same number for fixed delays (e.g., both to `2` for exactly 2 seconds)
- Set both to `0` for no delay

### Wallet Shuffling
Randomize the order of wallet processing:
- Set `SHUFFLE_WALLETS=true` to enable shuffling
- Set `SHUFFLE_WALLETS=false` to process wallets in file order

## Security Considerations

- The `data/private_keys.txt` file contains sensitive information. Keep it secure.
- A `.gitignore` file is provided to prevent accidentally committing your private keys.
- Use dedicated wallets with minimal funds for these transactions. 

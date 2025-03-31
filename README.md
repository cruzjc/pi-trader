# Pi-Trader

An automated day trading system designed to run on Raspberry Pi, leveraging Alpaca Trading API and ChatGPT for intelligent trading decisions.

## Features

- Automated trading during US market hours
- Configurable trading intervals (default: 4 minutes)
- AI-powered trading decisions using ChatGPT
- Real-time portfolio management
- Easy configuration through environment variables
- Comprehensive logging system

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the config directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ALPACA_API_KEY=your_alpaca_api_key
   ALPACA_SECRET_KEY=your_alpaca_secret_key
   ALPACA_ENDPOINT=https://paper-api.alpaca.markets  # Use paper trading for testing
   TRADING_INTERVAL=4  # Trading interval in minutes
   ```

## Running the System

1. Ensure all configurations are set in the `.env` file
2. Run the main script:
   ```bash
   python src/main.py
   ```

The system will automatically:
- Start at market open (9:30 AM EST)
- Make trading decisions at specified intervals
- Log all activities and trades
- Close positions at market close (4:00 PM EST)

## Logs

All trading activities are logged in the `logs` directory:
- `trading.log`: Contains all trading decisions and executions
- `error.log`: Contains any errors or warnings

## Configuration

You can modify the following parameters in the `.env` file:
- `TRADING_INTERVAL`: Time between trades in minutes
- `MAX_POSITION_SIZE`: Maximum position size per trade
- `RISK_LEVEL`: Risk level for trading (1-5)

## Disclaimer

This is an experimental trading system. Use at your own risk. Paper trading is recommended for testing. 
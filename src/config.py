import os
from dotenv import load_dotenv
import pytz

# Load environment variables from config/.env
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
load_dotenv(env_path)

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_ENDPOINT = os.getenv('ALPACA_ENDPOINT', 'https://paper-api.alpaca.markets')

# Trading Configuration
TRADING_INTERVAL = int(os.getenv('TRADING_INTERVAL', '4'))  # minutes
MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', '10000'))  # dollars
RISK_LEVEL = int(os.getenv('RISK_LEVEL', '3'))  # 1-5

# Market Hours (EST)
EST_TZ = pytz.timezone('US/Eastern')
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MINUTE = 0

# Logging Configuration
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
TRADING_LOG_FILE = os.path.join(LOG_DIR, 'trading.log')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'error.log')

# ChatGPT System Prompt
TRADING_SYSTEM_PROMPT = """You are an experienced day trader and financial analyst. Your role is to make trading decisions based on:
1. Current market conditions
2. Portfolio positions
3. Recent price movements
4. Trading history

Guidelines for decision making:
- Analyze the provided market data objectively
- Consider both technical and fundamental factors
- Manage risk by suggesting position sizes
- Provide clear reasoning for each trade decision
- Be mindful of market volatility and trends
- Consider the overall portfolio balance

For each trade recommendation, provide:
1. The action (BUY/SELL)
2. The ticker symbol
3. The quantity or position size
4. A brief explanation of the reasoning
5. Any relevant risk factors

Remember to maintain a balanced portfolio and never risk more than the specified position size.""" 
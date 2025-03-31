import logging
from datetime import datetime
import pytz
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import openai
from . import config

class PiTrader:
    def __init__(self):
        # Initialize logging
        self._setup_logging()
        
        # Initialize API clients
        self.trading_client = TradingClient(
            config.ALPACA_API_KEY,
            config.ALPACA_SECRET_KEY,
            paper=True if 'paper' in config.ALPACA_ENDPOINT else False
        )
        
        self.data_client = StockHistoricalDataClient(
            config.ALPACA_API_KEY,
            config.ALPACA_SECRET_KEY
        )
        
        self.openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        
        self.logger.info("PiTrader initialized successfully")

    def _setup_logging(self):
        """Configure logging for the trading system"""
        self.logger = logging.getLogger('PiTrader')
        self.logger.setLevel(logging.INFO)
        
        # Trading log handler
        trading_handler = logging.FileHandler(config.TRADING_LOG_FILE)
        trading_handler.setLevel(logging.INFO)
        trading_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        trading_handler.setFormatter(trading_formatter)
        self.logger.addHandler(trading_handler)
        
        # Error log handler
        error_handler = logging.FileHandler(config.ERROR_LOG_FILE)
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)

    def is_market_open(self):
        """Check if the market is currently open"""
        clock = self.trading_client.get_clock()
        return clock.is_open

    def get_market_data(self):
        """Gather current market data and portfolio positions"""
        try:
            account = self.trading_client.get_account()
            positions = self.trading_client.get_all_positions()
            
            # Get some basic market data for major indices
            indices = ['SPY', 'QQQ', 'IWM']
            market_data = {}
            
            for symbol in indices:
                request = StockBarsRequest(
                    symbol_or_symbols=symbol,
                    timeframe=TimeFrame.Hour,
                    start=datetime.now(pytz.UTC).replace(hour=0, minute=0, second=0, microsecond=0),
                )
                bars = self.data_client.get_stock_bars(request)
                if bars:
                    market_data[symbol] = bars[symbol][-1].close
            
            return {
                'account_value': float(account.equity),
                'buying_power': float(account.buying_power),
                'positions': [{
                    'symbol': pos.symbol,
                    'qty': float(pos.qty),
                    'current_price': float(pos.current_price),
                    'market_value': float(pos.market_value),
                    'unrealized_pl': float(pos.unrealized_pl)
                } for pos in positions],
                'market_indices': market_data
            }
        except Exception as e:
            self.logger.error(f"Error getting market data: {str(e)}")
            return None

    def get_trading_decision(self, market_data):
        """Get trading decision from ChatGPT"""
        try:
            message_content = f"""
Current Portfolio Status:
Account Value: ${market_data['account_value']:,.2f}
Buying Power: ${market_data['buying_power']:,.2f}

Current Positions:
{self._format_positions(market_data['positions'])}

Market Indices:
{self._format_market_indices(market_data['market_indices'])}

Based on this information, what trading actions should be taken?
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": config.TRADING_SYSTEM_PROMPT},
                    {"role": "user", "content": message_content}
                ],
                temperature=0.7
            )
            
            decision = response.choices[0].message.content
            self.logger.info(f"Trading decision received: {decision}")
            return decision
            
        except Exception as e:
            self.logger.error(f"Error getting trading decision: {str(e)}")
            return None

    def execute_trade(self, symbol, side, quantity):
        """Execute a trade based on the decision"""
        try:
            order_request = MarketOrderRequest(
                symbol=symbol,
                qty=quantity,
                side=OrderSide.BUY if side.upper() == 'BUY' else OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            )
            
            order = self.trading_client.submit_order(order_request)
            self.logger.info(f"Order submitted: {side} {quantity} shares of {symbol}")
            return order
            
        except Exception as e:
            self.logger.error(f"Error executing trade: {str(e)}")
            return None

    def _format_positions(self, positions):
        """Format positions data for ChatGPT prompt"""
        if not positions:
            return "No open positions"
        
        return "\n".join([
            f"- {p['symbol']}: {p['qty']} shares @ ${p['current_price']:.2f} "
            f"(Value: ${p['market_value']:.2f}, P/L: ${p['unrealized_pl']:.2f})"
            for p in positions
        ])

    def _format_market_indices(self, indices):
        """Format market indices data for ChatGPT prompt"""
        return "\n".join([
            f"- {symbol}: ${price:.2f}"
            for symbol, price in indices.items()
        ])

    def close_all_positions(self):
        """Close all open positions"""
        try:
            self.trading_client.close_all_positions(cancel_orders=True)
            self.logger.info("All positions closed")
        except Exception as e:
            self.logger.error(f"Error closing positions: {str(e)}") 
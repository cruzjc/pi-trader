import time
import schedule
from datetime import datetime, timedelta
import re
import logging
from trader import PiTrader
from config import (
    TRADING_INTERVAL,
    EST_TZ,
    MARKET_OPEN_HOUR,
    MARKET_OPEN_MINUTE,
    MARKET_CLOSE_HOUR,
    MARKET_CLOSE_MINUTE
)

def parse_trading_decision(decision):
    """Parse the trading decision from ChatGPT response"""
    # Look for patterns like "BUY 100 shares of AAPL" or "SELL 50 TSLA"
    patterns = [
        r'(BUY|SELL)\s+(\d+)\s+(?:shares\s+of\s+)?([A-Z]+)',
        r'(BUY|SELL)\s+([A-Z]+)\s+(\d+)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, decision, re.IGNORECASE)
        for match in matches:
            groups = match.groups()
            if len(groups) == 3:
                side = groups[0].upper()
                symbol = groups[2] if pattern.endswith('([A-Z]+)') else groups[1]
                quantity = int(groups[1] if pattern.endswith('([A-Z]+)') else groups[2])
                return side, symbol, quantity
    
    return None, None, None

def trading_job(trader):
    """Execute one trading cycle"""
    try:
        # Check if market is open
        if not trader.is_market_open():
            trader.logger.info("Market is closed. Skipping trading cycle.")
            return

        # Get market data
        market_data = trader.get_market_data()
        if not market_data:
            trader.logger.error("Failed to get market data. Skipping trading cycle.")
            return

        # Get trading decision
        decision = trader.get_trading_decision(market_data)
        if not decision:
            trader.logger.error("Failed to get trading decision. Skipping trading cycle.")
            return

        # Parse and execute trading decision
        side, symbol, quantity = parse_trading_decision(decision)
        if side and symbol and quantity:
            trader.execute_trade(symbol, side, quantity)
        else:
            trader.logger.info("No actionable trading signals found in the decision.")

    except Exception as e:
        trader.logger.error(f"Error in trading cycle: {str(e)}")

def market_close_job(trader):
    """Close all positions at market close"""
    trader.logger.info("Market closing - closing all positions")
    trader.close_all_positions()

def run_trading_system():
    """Main function to run the trading system"""
    trader = PiTrader()
    
    # Schedule trading job
    schedule.every(TRADING_INTERVAL).minutes.do(trading_job, trader=trader)
    
    # Schedule market close job
    market_close_time = f"{MARKET_CLOSE_HOUR:02d}:{MARKET_CLOSE_MINUTE:02d}"
    schedule.every().day.at(market_close_time).do(market_close_job, trader=trader)
    
    trader.logger.info(f"Trading system started. Trading interval: {TRADING_INTERVAL} minutes")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            trader.logger.info("Trading system stopped by user")
            trader.close_all_positions()
            break
        except Exception as e:
            trader.logger.error(f"Unexpected error: {str(e)}")
            time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    run_trading_system() 
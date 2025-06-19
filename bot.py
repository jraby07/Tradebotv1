import argparse
import json
import os
import time
from dataclasses import dataclass
from typing import List, Tuple

import ccxt
import pandas as pd
from rich.console import Console
from rich.table import Table

from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

console = Console()

@dataclass
class Trade:
    action: str
    price: float
    amount: float
    reason: str
    pnl: float = 0.0
    open: bool = True
    stop_loss: float = 0.0
    take_profit: float = 0.0

class TradeBot:
    def __init__(self, config: dict, simulate: bool = True):
        self.config = config
        self.simulate = simulate
        self.exchange = ccxt.coinbasepro({
            'apiKey': os.environ.get('COINBASE_API_KEY'),
            'secret': os.environ.get('COINBASE_API_SECRET'),
            'password': os.environ.get('COINBASE_API_PASSPHRASE')
        })
        self.trades: List[Trade] = []
        self.aggressiveness = int(self.config.get('aggressiveness', 5))
        self.balance = float(self.config.get('starting_balance', 10000))
        self.running = False


    def fetch_news_sentiment(self) -> float:
        """Placeholder for news sentiment analysis."""
        # In a production bot, fetch and analyze recent crypto news here.
        return 0.0

    def calculate_trade_amount(self, price: float) -> float:
        max_pct = self.config['max_trade_percentage'] / 100
        pct = max_pct * (self.aggressiveness / 10)
        usd = self.balance * pct
        return usd / price

    def fetch_ohlc(self, symbol: str, timeframe: str = '1h', limit: int = 200) -> pd.DataFrame:
        """Fetch historical candlestick data."""
        ohlc = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlc, columns=['timestamp','open','high','low','close','volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def apply_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        rsi_cfg = self.config['indicators']['RSI']
        macd_cfg = self.config['indicators']['MACD']
        bb_cfg = self.config['indicators']['BollingerBands']

        df['rsi'] = RSIIndicator(close=df['close'], window=rsi_cfg['period']).rsi()
        macd = MACD(close=df['close'],
                    window_slow=macd_cfg['slow_period'],
                    window_fast=macd_cfg['fast_period'],
                    window_sign=macd_cfg['signal_period'])
        df['macd'] = macd.macd_diff()
        bb = BollingerBands(close=df['close'],
                            window=bb_cfg['period'],
                            window_dev=bb_cfg['stdDev'])
        df['bb_low'] = bb.bollinger_lband()
        df['bb_high'] = bb.bollinger_hband()
        return df

    def generate_signal(self, df: pd.DataFrame) -> Tuple[str, str]:
        last = df.iloc[-1]
        reasons = []
        signal = None
        sentiment = self.fetch_news_sentiment()
        if sentiment < -0.5:
            return None, 'negative news sentiment'
        if sentiment > 0.5:
            reasons.append('positive news sentiment')
        if last['rsi'] < self.config['indicators']['RSI']['oversold'] and last['close'] <= last['bb_low']:
            signal = 'buy'
            reasons.append('RSI oversold and price near lower Bollinger band')
        elif last['rsi'] > self.config['indicators']['RSI']['overbought'] and last['close'] >= last['bb_high']:
            signal = 'sell'
            reasons.append('RSI overbought and price near upper Bollinger band')
        return signal, '; '.join(reasons)

    def execute_trade(self, action: str, amount: float, price: float, reason: str):
        if self.simulate:
            console.log(f"Simulated {action} {amount} at {price} - {reason}")
        else:
            if action == 'buy':
                self.exchange.create_market_buy_order('BTC/USD', amount)
            else:
                self.exchange.create_market_sell_order('BTC/USD', amount)
        sl_pct = self.config['risk_management']['stop_loss_percentage'] / 100
        tp_pct = self.config['risk_management']['take_profit_percentage'] / 100
        if action == 'buy':
            stop = price * (1 - sl_pct)
            take = price * (1 + tp_pct)
        else:
            stop = price * (1 + sl_pct)
            take = price * (1 - tp_pct)
        self.trades.append(Trade(action, price, amount, reason, 0.0, True, stop, take))

    def update_pnl(self, current_price: float):
        for trade in self.trades:
            if trade.action == 'buy':
                trade.pnl = (current_price - trade.price) * trade.amount
            else:
                trade.pnl = (trade.price - current_price) * trade.amount

    def manage_trades(self, current_price: float):
        for trade in self.trades:
            if not trade.open:
                continue
            if trade.action == 'buy':
                if current_price <= trade.stop_loss or current_price >= trade.take_profit:
                    trade.pnl = (current_price - trade.price) * trade.amount
                    self.balance += trade.price * trade.amount + trade.pnl
                    trade.open = False
            else:
                if current_price >= trade.stop_loss or current_price <= trade.take_profit:
                    trade.pnl = (trade.price - current_price) * trade.amount
                    self.balance += trade.price * trade.amount + trade.pnl
                    trade.open = False

    def print_status(self):
        table = Table(title="Trade History")
        table.add_column("Action")
        table.add_column("Price", justify="right")
        table.add_column("Amount", justify="right")
        table.add_column("Reason")
        table.add_column("PnL", justify="right")
        for t in self.trades:
            table.add_row(t.action, f"{t.price:.2f}", f"{t.amount:.4f}", t.reason, f"{t.pnl:.2f}")
        console.print(table)
        bar = "█" * self.aggressiveness + " " * (10 - self.aggressiveness)
        console.print(f"Balance: {self.balance:.2f} | Aggressiveness: {self.aggressiveness}/10 [{bar}]")

    def run(self):
        symbol = 'BTC/USD'
        while True:
    def stop(self):
        """Stop the bot loop."""
        self.running = False

    def get_status(self) -> dict:
        """Return current balance and trades for API usage."""
        trades = [
            {
                'action': t.action,
                'price': t.price,
                'amount': t.amount,
                'reason': t.reason,
                'pnl': t.pnl,
                'open': t.open,
                'stop_loss': t.stop_loss,
                'take_profit': t.take_profit,
            }
            for t in self.trades
        ]
        return {
            'balance': self.balance,
            'aggressiveness': self.aggressiveness,
            'trades': trades,
            'running': self.running,
        }

    def run(self):
        self.running = True
        symbol = 'BTC/USD'
        while self.running:
            df = self.fetch_ohlc(symbol)
            df = self.apply_indicators(df)
            signal, reason = self.generate_signal(df)
            last_price = df.iloc[-1]['close']
            if signal:
                amount = self.calculate_trade_amount(last_price)
                self.execute_trade(signal, amount, last_price, reason)
            self.update_pnl(last_price)
            self.manage_trades(last_price)
            self.print_status()
            time.sleep(60)


def load_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Simple trading bot")
    parser.add_argument('--mode', choices=['simulate', 'live'], default='simulate')
    parser.add_argument('--config', default='config.json')
    args = parser.parse_args()

    config = load_config(args.config)
    simulate = args.mode == 'simulate'
    console.log(f"Starting bot in {'simulation' if simulate else 'live'} mode")
    bot = TradeBot(config, simulate=simulate)
    bot.run()


if __name__ == '__main__':
    main()

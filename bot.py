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

class TradeBot:
    def __init__(self, config: dict, simulate: bool = True):
        self.config = config
        self.simulate = simulate
        exchange_name = config.get('exchange', 'coinbase').lower()
        if exchange_name == 'coinbase':
            api_key = os.environ.get('COINBASE_ADVANCED_API_KEY') or os.environ.get('COINBASE_API_KEY')
            api_secret = os.environ.get('COINBASE_ADVANCED_API_SECRET') or os.environ.get('COINBASE_API_SECRET')
            passphrase = os.environ.get('COINBASE_ADVANCED_API_PASSPHRASE') or os.environ.get('COINBASE_API_PASSPHRASE')
            self.exchange = ccxt.coinbase({
                'apiKey': api_key,
                'secret': api_secret,
                'password': passphrase
            })
        elif exchange_name == 'binance':
            self.exchange = ccxt.binance({
                'apiKey': os.environ.get('BINANCE_API_KEY'),
                'secret': os.environ.get('BINANCE_API_SECRET')
            })
        else:
            raise ValueError(f"Unsupported exchange: {exchange_name}")
        self.trades: List[Trade] = []
        self.last_row = None

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
        self.trades.append(Trade(action, price, amount, reason))

    def update_pnl(self, current_price: float):
        for trade in self.trades:
            if trade.action == 'buy':
                trade.pnl = (current_price - trade.price) * trade.amount
            else:
                trade.pnl = (trade.price - current_price) * trade.amount

    def success_rate(self) -> float:
        if not self.trades:
            return 0.0
        wins = sum(1 for t in self.trades if t.pnl >= 0)
        return wins / len(self.trades) * 100

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

    def run(self):
        symbol = 'BTC/USD'
        while True:
            df = self.fetch_ohlc(symbol)
            df = self.apply_indicators(df)
            signal, reason = self.generate_signal(df)
            last_price = df.iloc[-1]['close']
            self.last_row = df.iloc[-1].to_dict()
            if signal:
                amount = 0.001  # placeholder amount
                self.execute_trade(signal, amount, last_price, reason)
            self.update_pnl(last_price)
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

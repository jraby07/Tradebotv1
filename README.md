# Tradebotv1

Tradebotv1 is a small experimental cryptocurrency trading bot. The
project now includes a basic framework for executing a strategy using
technical indicators such as RSI, MACD and Bollinger Bands. The bot can
run in either **simulation** mode or **live** mode against Coinbase Pro.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `sample_config.json` to `config.json` and adjust the settings
   as needed.
3. Set the Coinbase API credentials as environment variables:
   - `COINBASE_API_KEY`
   - `COINBASE_API_SECRET`
   - `COINBASE_API_PASSPHRASE`

## Running

```
python bot.py --mode simulate   # dry run
python bot.py --mode live       # trade with real funds
```


### Web Interface

You can control the bot through a small web UI that also works as a
Progressive Web App (PWA).

```bash
python webapp.py
```

Open `http://localhost:5000` in your browser to start or stop the bot
and view its status.


The console output shows open positions and profit/loss for each trade.
This codebase is **not** production ready and should be used with
caution. Review the source and extend the trading logic and risk
management before trading with real money.

### Configuration highlights

- `aggressiveness` from 1-10 controls how large each trade is as a
  percentage of your balance. The default is 5.
- `starting_balance` sets the simulated initial capital.
- `market_type` may be `spot` or `futures` and determines which market
  the bot trades on via ccxt.

The strategy is very simple and does **not** guarantee profits. Use at
your own risk and consider consulting a financial professional before
trading with real funds.


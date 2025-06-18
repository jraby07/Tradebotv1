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

The console output shows open positions and profit/loss for each trade.
This codebase is **not** production ready and should be used with
caution. Review the source and extend the trading logic and risk
management before trading with real money.


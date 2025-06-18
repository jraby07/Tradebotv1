# Tradebotv1

Tradebotv1 is a small experimental cryptocurrency trading bot. The
project now includes a basic framework for executing a strategy using
technical indicators such as RSI, MACD and Bollinger Bands. The bot can
run in either **simulation** mode or **live** mode against Coinbase Pro.

Email reports are sent automatically at 5:00 and 17:00.

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

While running, open `http://localhost:8000` in a browser to toggle
between simulation and live modes.

The console output shows open positions and profit/loss for each trade.

### Configuration highlights

- `aggressiveness` from 1-10 controls how large each trade is as a
  percentage of your balance. The default is 5.
- `starting_balance` sets the simulated initial capital.
- `market_type` may be `spot` or `futures` and determines which market
  the bot trades on via ccxt.
- `switch_password` protects the toggle between simulation and live
  trading via the web interface.
- `email` holds SMTP settings for the daily reports.



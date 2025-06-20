# Tradebotv1

Tradebotv1 is an experimental cryptocurrency trading bot that can run in
**simulation** or **live** mode. It fetches data from Coinbase or
Binance, applies simple indicators (RSI, MACD and Bollinger Bands) and
executes trades. A small web interface can start the bot in either mode
and display recent trades.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `sample_config.json` to `config.json` and adjust the settings as
   needed. Set `exchange` to either `coinbase` or `binance`.
   The file also lets you specify a `starting_balance` for simulations and
   risk management settings like `stop_loss_percentage` and
   `take_profit_percentage`.
3. Export your exchange credentials as environment variables.
   - For Coinbase Advanced Trade:
     - `COINBASE_ADVANCED_API_KEY`
     - `COINBASE_ADVANCED_API_SECRET`
     - `COINBASE_ADVANCED_API_PASSPHRASE`
   - For Binance:
     - `BINANCE_API_KEY`
     - `BINANCE_API_SECRET`
4. Run `python webapp.py` to launch the browser interface.

## Running

```
python bot.py --mode simulate   # dry run
python bot.py --mode live       # trade with real funds
```

To control the bot through a browser, run:

```bash
python webapp.py
```

Open `http://localhost:8000` to start or stop the bot and switch
between simulation and live modes. The page refreshes automatically to
show the most recent indicator values, success rate and color-coded
trade history. When running in simulation mode the interface also shows
your virtual account balance.

The console output shows open positions and profit/loss for each trade.
This codebase is **not** production ready and should be used with
caution. Review the source and extend the trading logic and risk
management before trading with real money.


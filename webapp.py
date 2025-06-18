import threading
import time
from flask import Flask, redirect, render_template_string, request
from bot import TradeBot, load_config

app = Flask(__name__)

bot_thread = None
running_bot = None

TEMPLATE = """
<!doctype html>
<title>Tradebotv1</title>
<h1>Tradebotv1 Control</h1>
<form method="post" action="/start">
  Mode: <select name="mode">
    <option value="simulate">simulate</option>
    <option value="live">live</option>
  </select>
  <button type="submit">Start</button>
</form>
<form method="post" action="/stop">
  <button type="submit">Stop</button>
</form>
{% if indicators %}
<h2>Latest Indicators</h2>
<ul>
  <li>Price: {{ '%.2f' % indicators.close }}</li>
  <li>RSI: {{ '%.2f' % indicators.rsi }}</li>
  <li>MACD: {{ '%.2f' % indicators.macd }}</li>
  <li>Bollinger Low: {{ '%.2f' % indicators.bb_low }}</li>
  <li>Bollinger High: {{ '%.2f' % indicators.bb_high }}</li>
</ul>
{% endif %}

{% if trades %}
<h2>Trades (success rate: {{ '%.1f' % success_rate }}%)</h2>
<table border="1" cellpadding="5" style="border-collapse:collapse;">
<tr><th>Action</th><th>Price</th><th>Amount</th><th>Reason</th><th>PnL</th></tr>
{% for t in trades %}
<tr class="{{ 'win' if t.pnl >= 0 else 'loss' }}"><td>{{t.action}}</td><td>{{"%.2f" % t.price}}</td><td>{{"%.4f" % t.amount}}</td><td>{{t.reason}}</td><td>{{"%.2f" % t.pnl}}</td></tr>
{% endfor %}
</table>
{% endif %}

<style>
  .win { background-color: #c8e6c9; }
  .loss { background-color: #ffcdd2; }
</style>
"""


def start_bot(mode):
    global bot_thread, running_bot
    if bot_thread and bot_thread.is_alive():
        return
    config = load_config('config.json')
    simulate = mode == 'simulate'
    running_bot = TradeBot(config, simulate=simulate)

    def run_bot():
        running_bot.run()
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()


def stop_bot():
    global bot_thread, running_bot
    running_bot = None
    bot_thread = None


@app.route('/')
def index():
    trades = running_bot.trades if running_bot else []
    indicators = running_bot.last_row if running_bot else None
    success = running_bot.success_rate() if running_bot else 0.0
    return render_template_string(TEMPLATE, trades=trades,
                                  indicators=indicators,
                                  success_rate=success)


@app.route('/start', methods=['POST'])
def start():
    mode = request.form.get('mode', 'simulate')
    start_bot(mode)
    time.sleep(1)
    return redirect('/')


@app.route('/stop', methods=['POST'])
def stop():
    stop_bot()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


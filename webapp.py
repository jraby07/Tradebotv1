import threading
import time
from flask import Flask, redirect, render_template_string, request, jsonify
from bot import TradeBot, load_config

app = Flask(__name__)

bot_thread = None
running_bot = None

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Tradebotv1</title>
  <style>
    body { font-family: Arial, sans-serif; }
    table { border-collapse: collapse; width: 100%; margin-top: 10px; }
    th, td { border: 1px solid #ccc; padding: 4px; text-align: left; }
    .win { background-color: #c8e6c9; }
    .loss { background-color: #ffcdd2; }
  </style>
</head>
<body>
<h1>Tradebotv1 Control</h1>
<form id="startForm" method="post" action="/start">
  Mode: <select name="mode" id="mode">
    <option value="simulate">simulate</option>
    <option value="live">live</option>
  </select>
  <button type="submit">Start</button>
  <button type="button" id="stopBtn">Stop</button>
</form>

<h2>Latest Indicators</h2>
<ul id="indicators">
  <li>Price: <span id="price">-</span></li>
  <li>RSI: <span id="rsi">-</span></li>
  <li>MACD: <span id="macd">-</span></li>
  <li>Bollinger Low: <span id="bb_low">-</span></li>
  <li>Bollinger High: <span id="bb_high">-</span></li>
  <li>Balance: <span id="balance">-</span></li>
</ul>

<h2>Trades (<span id="success">0</span>% success)</h2>
<table id="trades">
  <thead>
    <tr><th>Action</th><th>Price</th><th>Amount</th><th>Reason</th><th>PnL</th></tr>
  </thead>
  <tbody></tbody>
</table>

<script>
async function fetchStatus() {
  const r = await fetch('/status');
  if (!r.ok) return;
  const data = await r.json();
  document.getElementById('success').textContent = data.success_rate.toFixed(1);
  if (data.indicators) {
    document.getElementById('price').textContent = data.indicators.close.toFixed(2);
    document.getElementById('rsi').textContent = data.indicators.rsi.toFixed(2);
    document.getElementById('macd').textContent = data.indicators.macd.toFixed(2);
    document.getElementById('bb_low').textContent = data.indicators.bb_low.toFixed(2);
    document.getElementById('bb_high').textContent = data.indicators.bb_high.toFixed(2);
  }
  if (data.balance !== undefined) {
    document.getElementById('balance').textContent = data.balance.toFixed(2);
  }
  const tbody = document.querySelector('#trades tbody');
  tbody.innerHTML = '';
  for (const t of data.trades) {
    const row = document.createElement('tr');
    row.className = t.pnl >= 0 ? 'win' : 'loss';
    row.innerHTML = `<td>${t.action}</td><td>${t.price.toFixed(2)}</td><td>${t.amount.toFixed(4)}</td><td>${t.reason}</td><td>${t.pnl.toFixed(2)}</td>`;
    tbody.appendChild(row);
  }
}

document.getElementById('stopBtn').onclick = async function() {
  await fetch('/stop', {method: 'POST'});
};

setInterval(fetchStatus, 5000);
fetchStatus();
</script>
</body>
</html>
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
    balance = running_bot.balance if running_bot else None
    return render_template_string(TEMPLATE, trades=trades,
                                  indicators=indicators,
                                  success_rate=success,
                                  balance=balance)


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


@app.route('/status')
def status():
    trades = running_bot.trades if running_bot else []
    indicators = running_bot.last_row if running_bot else None
    success = running_bot.success_rate() if running_bot else 0.0
    return jsonify({
        'trades': [t.__dict__ for t in trades],
        'indicators': indicators,
        'success_rate': success,
        'balance': running_bot.balance if running_bot else None
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


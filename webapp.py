from threading import Thread

from flask import Flask, jsonify, request, send_from_directory

from bot import TradeBot, load_config

app = Flask(__name__, static_folder='static', static_url_path='')

bot = None
bot_thread = None

@app.route('/api/start', methods=['POST'])
def start_bot():
    global bot, bot_thread
    if bot and bot.running:
        return jsonify({'status': 'running'})
    cfg_path = request.json.get('config', 'config.json')
    mode = request.json.get('mode', 'simulate')
    config = load_config(cfg_path)
    bot = TradeBot(config, simulate=(mode == 'simulate'))
    bot_thread = Thread(target=bot.run, daemon=True)
    bot_thread.start()
    return jsonify({'status': 'started'})

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    global bot
    if bot:
        bot.stop()
    return jsonify({'status': 'stopped'})

@app.route('/api/status')
def status():
    if bot:
        return jsonify(bot.get_status())
    return jsonify({'running': False})

@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

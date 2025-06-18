import json
import os
import time

def main():
    print("MoneyMaker5000 bot starting up...")
    config_path = os.getenv("CONFIG_PATH", "config.json")
    with open(config_path) as f:
        config = json.load(f)
    print("Config loaded. Running in", config["trade_mode"], "mode.")

    # Main trading loop (placeholder)
    while True:
        print("Simulating trade logic...")
        time.sleep(60)

if __name__ == "__main__":
    main()

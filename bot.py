import json
import time

def main():
    print("MoneyMaker5000 bot starting up...")
    with open("config.json") as f:
        config = json.load(f)
    print("Config loaded. Running in", config["trade_mode"], "mode.")

    # Main trading loop (placeholder)
    while True:
        print("Simulating trade logic...")
        time.sleep(60)

if __name__ == "__main__":
    main()
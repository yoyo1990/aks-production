import threading
import time
import requests
from collections import deque
from datetime import datetime
from flask import Flask, jsonify

FETCH_INTERVAL = 60  # seconds
SAMPLES = 10  # minutes window

app = Flask(__name__)
prices = deque(maxlen=SAMPLES)
lock = threading.Lock()

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"


def fetch_loop():
    while True:
        try:
            r = requests.get(COINGECKO_API, timeout=10)
            r.raise_for_status()
            data = r.json()
            price = float(data["bitcoin"]["usd"])
            with lock:
                prices.append((datetime.utcnow().isoformat() + "Z", price))
            print(f"[{datetime.utcnow().isoformat()}] BTC={price} USD | samples={len(prices)}")
        except Exception as e:
            print(f"[{datetime.utcnow().isoformat()}] fetch error: {e}")
        time.sleep(FETCH_INTERVAL)


@app.route("/metrics")
def metrics():
    with lock:
        if not prices:
            return jsonify({"samples": 0}), 200
        last_ts, last_price = prices[-1]
        avg = sum(p for _, p in prices) / len(prices)
        return jsonify({
            "last_timestamp": last_ts,
            "last_price": last_price,
            "moving_average": avg,
            "samples": len(prices)
        })


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/ready")
def ready():
    # ready when we have at least 1 sample
    with lock:
        return ("ready", 200) if prices else ("not ready", 503)


if __name__ == "__main__":
    # Start background fetcher
    t = threading.Thread(target=fetch_loop, daemon=True)
    t.start()
    # Start Flask
    app.run(host="0.0.0.0", port=8080)

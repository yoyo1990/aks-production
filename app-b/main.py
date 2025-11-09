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


@app.route("/")
def home():
    with lock:
        if not prices:
            data = {
                "service": "Bitcoin Price Service B",
                "status": "initializing",
                "samples": 0,
                "price": None,
                "average": None
            }
        else:
            last_ts, last_price = prices[-1]
            avg = sum(p for _, p in prices) / len(prices)
            data = {
                "service": "Bitcoin Price Service B",
                "status": "active",
                "last_timestamp": last_ts,
                "last_price": last_price,
                "moving_average": avg,
                "samples": len(prices),
                "price": last_price,
                "average": round(avg, 2)
            }
        
        # Return beautiful HTML page with different color scheme
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="he">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🪙 Bitcoin Price Monitor - Service B</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #2196F3 0%, #21CBF3 100%);
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                    direction: rtl;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .bitcoin-logo {{
                    width: 80px;
                    height: 80px;
                    background: linear-gradient(135deg, #2196F3, #64B5F6);
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 40px;
                    margin-bottom: 15px;
                    color: white;
                }}
                .title {{
                    color: #333;
                    margin: 10px 0;
                    font-size: 2.5em;
                    font-weight: bold;
                }}
                .service-name {{
                    color: #666;
                    font-size: 1.2em;
                    margin-bottom: 20px;
                }}
                .cards {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-top: 30px;
                }}
                .card {{
                    background: white;
                    padding: 25px;
                    border-radius: 15px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
                    border-left: 5px solid #2196F3;
                    transition: transform 0.3s ease;
                }}
                .card:hover {{
                    transform: translateY(-5px);
                }}
                .card-title {{
                    font-size: 1em;
                    color: #666;
                    margin-bottom: 10px;
                    text-transform: uppercase;
                    font-weight: bold;
                    letter-spacing: 1px;
                }}
                .card-value {{
                    font-size: 2.2em;
                    font-weight: bold;
                    color: #333;
                    margin: 10px 0;
                }}
                .price {{
                    color: #4CAF50;
                }}
                .average {{
                    color: #2196F3;
                }}
                .status {{
                    color: #4CAF50;
                }}
                .samples {{
                    color: #6c757d;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 0.9em;
                }}
                .status-badge {{
                    display: inline-block;
                    padding: 5px 15px;
                    border-radius: 20px;
                    background: #2196F3;
                    color: white;
                    font-size: 0.8em;
                    font-weight: bold;
                    margin-top: 10px;
                }}
                .refresh-info {{
                    background: rgba(33, 150, 243, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    margin-top: 20px;
                    text-align: center;
                    color: #2196F3;
                }}
                .service-b-badge {{
                    background: linear-gradient(135deg, #2196F3, #64B5F6);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    display: inline-block;
                    margin-bottom: 20px;
                    font-weight: bold;
                }}
            </style>
            <script>
                // Auto refresh every 30 seconds
                setInterval(function() {{
                    location.reload();
                }}, 30000);
            </script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="bitcoin-logo">₿</div>
                    <h1 class="title">מעקב מחיר ביטקוין</h1>
                    <div class="service-b-badge">🔵 שירות B - מסד נתונים משני</div>
                </div>
                
                <div class="cards">
                    <div class="card">
                        <div class="card-title">💎 מחיר נוכחי</div>
                        <div class="card-value price">
                            {"$" + f"{data['price']:,.2f}" if data['price'] else "טוען..."}
                        </div>
                        <div class="status-badge">{"פעיל" if data['status'] == 'active' else "מאתחל"}</div>
                    </div>
                    
                    <div class="card">
                        <div class="card-title">📊 ממוצע נע</div>
                        <div class="card-value average">
                            {"$" + f"{data['average']:,.2f}" if data.get('average') else "טוען..."}
                        </div>
                        <small>ממוצע 10 דקות אחרונות</small>
                    </div>
                    
                    <div class="card">
                        <div class="card-title">🔢 דגימות</div>
                        <div class="card-value samples">{data['samples']}/10</div>
                        <small>נתונים שנאספו</small>
                    </div>
                    
                    <div class="card">
                        <div class="card-title">⚡ סטטוס מערכת</div>
                        <div class="card-value status">{"🔵 מחובר" if data['status'] == 'active' else "🟡 מתחבר"}</div>
                        <small>שירות B פעיל</small>
                    </div>
                </div>
                
                <div class="refresh-info">
                    🔄 רענון אוטומטי כל 30 שניות
                    <br>
                    📊 שירות גיבוי ומעקב משני
                </div>
                
                <div class="footer">
                    <p>🌐 Azure Kubernetes Service | 🛡️ Secured by nginx | 🔐 Authenticated Access</p>
                    <p>Service B - עדכון אחרון: {data.get('last_timestamp', 'N/A')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html


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
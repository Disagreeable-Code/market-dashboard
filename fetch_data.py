import yfinance as yf
import json


TICKERS = {
    "S&P 500":     "^GSPC",
    "Dow Jones":   "^DJI",
    "Nasdaq":      "^IXIC",
    "Crude Oil":   "CL=F",
    "Natural Gas": "NG=F",
    "Gold":        "GC=F",
    "Copper":      "HG=F",
    "Wheat":       "ZW=F",
    "OJ Futures":  "OJ=F",
}

data = {}

for name, symbol in TICKERS.items():
    try:
        hist = yf.Ticker(symbol).history(period="1mo")
        data[name] = {
            "price": round(hist["Close"].iloc[-1], 2),
            "dates": hist.index.strftime("%Y-%m-%d").tolist(),
            "closes": [round(x, 2) for x in hist["Close"].tolist()]
        }
    except Exception as e:
        data[name] = None
        print(f"Failed to fetch {name}: {e}")



rows = ""
for name, d in data.items():
    if d:
        rows += f"<tr><td>{name}</td><td>${d['price']}</td></tr>\n"

charts = ""
for name, d in data.items():
    if d:
        chart_id = name.replace(" ", "_").replace("&", "")
        charts += f"""
        <div class="chart-box">
            <div id="{chart_id}"></div>
        </div>
        <script>
            Plotly.newPlot("{chart_id}", [{{
                x: {json.dumps(d['dates'])},
                y: {json.dumps(d['closes'])},
                type: "scatter",
                name: "{name}",
                line: {{color: "#00ff99"}}
            }}], {{
                title: "{name}",
                paper_bgcolor: "#1a1a2e",
                plot_bgcolor: "#16213e",
                font: {{color: "#ffffff"}},
                margin: {{t: 40, b: 40, l: 50, r: 20}}
            }});
        </script>
        """

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Market Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            background: #1a1a2e;
            color: #ffffff;
            font-family: monospace;
            padding: 20px;
        }}
        h1 {{ color: #00ff99; }}
        table {{
            border-collapse: collapse;
            margin-bottom: 40px;
            width: 400px;
        }}
        th, td {{
            padding: 10px 20px;
            border: 1px solid #333;
            text-align: left;
        }}
        th {{ background: #16213e; color: #00ff99; }}
        tr:hover {{ background: #16213e; }}
        .chart-box {{
            display: inline-block;
            width: 500px;
            margin: 10px;
        }}
    </style>
</head>
<body>
    <h1>Market Dashboard</h1>
    <table>
        <tr><th>Asset</th><th>Price</th></tr>
        {rows}
    </table>
    {charts}
</body>
</html>
"""

with open("dashboard.html", "w") as f:
    f.write(html)

print("Dashboard written to dashboard.html")
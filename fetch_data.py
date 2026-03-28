import yfinance as yf
import json


TICKERS = {
    "S&P 500":           "^GSPC",
    "Dow Jones":         "^DJI",
    "Nasdaq":            "^IXIC",
    "Crude Oil":         "CL=F",
    "Natural Gas":       "NG=F",
    "Gold":              "GC=F",
    "Copper":            "HG=F",
    "Aluminum":          "ALI=F",   
    "Wheat":             "ZW=F",
    "OJ Futures":        "OJ=F",
    "Mosaic Co":         "MOS",
    "Nutrien":           "NTR",
    "2Y Treasury":       "^IRX",
    "10Y Treasury":      "^TNX",
    "30Y Treasury":      "^TYX"
}

data = {}

for name, symbol in TICKERS.items():
    try:
        hist_mo  = yf.Ticker(symbol).history(period="1mo")
        hist_ytd = yf.Ticker(symbol).history(period="1y")
        hist_5d  = yf.Ticker(symbol).history(period="5d", interval="1h")

        first_ytd = hist_ytd["Close"].iloc[0]
        first_5d  = hist_5d["Close"].iloc[0]

        data[name] = {
            "price":      round(hist_mo["Close"].iloc[-1], 2),
            "dates":      hist_mo.index.strftime("%Y-%m-%d").tolist(),
            "closes":     [round(x, 2) for x in hist_mo["Close"].tolist()],
            "ytd_dates":  hist_ytd.index.strftime("%Y-%m-%d").tolist(),
            "ytd_pct":    [round((x - first_ytd) / first_ytd * 100, 2)
                           for x in hist_ytd["Close"].tolist()],
            "5d_dates":   hist_5d.index.strftime("%Y-%m-%d %H:%M").tolist(),
            "5d_pct":     [round((x - first_5d) / first_5d * 100, 2)
                           for x in hist_5d["Close"].tolist()],
        }
    except Exception as e:
        data[name] = None
        print(f"Failed to fetch {name}: {e}")


rows = ""
for name, d in data.items():
    if d:
        rows += f"<tr><td>{name}</td><td>${d['price']}</td></tr>\n"


COLORS = [
    "#00ff99", "#ff6b6b", "#ffd93d", "#6bcbff",
    "#ff9f43", "#a29bfe", "#fd79a8", "#55efc4",
    "#fdcb6e", "#e17055", "#74b9ff", "#00cec9",
    "#fab1a0", "#81ecec", "#636e72"
]

ytd_traces = ""
d5_traces = ""
for i, (name, d) in enumerate(data.items()):
    if d:
        color = COLORS[i % len(COLORS)]
        ytd_traces += f"""{{
            x: {json.dumps(d['ytd_dates'])},
            y: {json.dumps(d['ytd_pct'])},
            type: "scatter",
            name: "{name}",
            line: {{color: "{color}"}}
        }},"""
        d5_traces += f"""{{
            x: {json.dumps(d['5d_dates'])},
            y: {json.dumps(d['5d_pct'])},
            type: "scatter",
            name: "{name}",
            line: {{color: "{color}"}}
        }},"""

composite_charts = f"""
<div id="ytd_composite" style="width:100%; height:500px; margin-bottom:40px;"></div>
<script>
    Plotly.newPlot("ytd_composite", [{ytd_traces}], {{
        title: "1 Year Performance (% change)",
        paper_bgcolor: "#1a1a2e",
        plot_bgcolor: "#16213e",
        font: {{color: "#ffffff"}},
        yaxis: {{title: "% Change", zeroline: true,
                 zerolinecolor: "#ffffff", zerolinewidth: 1}},
        margin: {{t: 50, b: 50, l: 60, r: 20}}
    }});
</script>

<div id="d5_composite" style="width:100%; height:500px; margin-bottom:40px;"></div>
<script>
    Plotly.newPlot("d5_composite", [{d5_traces}], {{
        title: "5 Day Performance (% change)",
        paper_bgcolor: "#1a1a2e",
        plot_bgcolor: "#16213e",
        font: {{color: "#ffffff"}},
        yaxis: {{title: "% Change", zeroline: true,
                 zerolinecolor: "#ffffff", zerolinewidth: 1}},
        margin: {{t: 50, b: 50, l: 60, r: 20}}
    }});
</script>
"""




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
    <div style="display:flex; gap:40px; align-items:flex-start;">
        <table>
            <tr><th>Asset</th><th>Price</th></tr>
            {rows}
        </table>
        <div style="flex:1;">
            {composite_charts}
        </div>
    </div>
    <div style="display:flex; flex-wrap:wrap;">
        {charts}
    </div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("Dashboard written to dashboard.html")
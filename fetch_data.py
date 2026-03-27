import yfinance as yf

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
        hist = yf.Ticker(symbol).history(period="1d")
        data[name] = round(hist["Close"].iloc[-1], 2)
    except Exception as e:
        data[name] = None
        print(f"Failed to fetch {name}: {e}")

rows = ""
for name, price in data.items():
    rows += f"<tr><td>{name}</td><td>{price}</td></tr>\n"

html = f"""
<!DOCTYPE html>
<html>
<body>
    <h1>Market Dashboard</h1>
    <table border="1">
        <tr><th>Asset</th><th>Price</th></tr>
        {rows}
    </table>
</body>
</html>
"""

with open("dashboard.html", "w") as f:
    f.write(html)

print("Dashboard written to dashboard.html")
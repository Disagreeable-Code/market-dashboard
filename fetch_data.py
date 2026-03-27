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

for name, price in data.items():
    print(f"{name}: {price}")
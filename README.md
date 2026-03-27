# Market Dashboard

Fetches live market data and generates a local HTML dashboard
with interactive charts.

## Tracked Assets

**Indices:** S&P 500, Dow Jones, Nasdaq
**Energy:** Crude Oil, Natural Gas
**Metals:** Gold, Copper
**Agriculture:** Wheat, OJ Futures

## Setup1

pip install -r requirements.txt


## Setup Isolated Environ

conda create -n market-dashboard python=3.11
conda activate market-dashboard
pip install -r requirements.txt


## Usage

python fetch_data.py
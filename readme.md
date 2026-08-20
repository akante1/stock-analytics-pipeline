# Stock Market Analytics Pipeline

An end-to-end data pipeline that ingests 5 years of daily market data for 20
stocks, stores it in a SQL database, transforms it with window functions and
CTEs, and surfaces insights through Python analysis and an interactive Tableau
dashboard.

**Dashboard:** [Live on Tableau Public](ADD-LINK-WHEN-PUBLISHED)

## Architecture

Yahoo Finance API
      │
      ▼
 fetch.py ──────► stock_prices.csv        (ingest: Python + yfinance)
      │
      ▼
 load.py ───────► stocks.db               (store: SQLite)
      │
      ▼
 analyze.py                               (transform: SQL window functions, CTEs)
 insights.py                              (analyze: pandas — correlation, drawdown, Sharpe)
      │
      ▼
 export_for_tableau.py ► tableau_data.csv (visualize: Tableau Public dashboard)

## Tech Stack

- **Python** — yfinance, pandas
- **SQL** — SQLite; window functions (`LAG`, sliding-window `AVG`), CTEs, aggregation
- **Tableau Public** — interactive dashboard
- **Git/GitHub** — version control

## Setup & Run

```bash
git clone https://github.com/akante1/stock-analytics-pipeline.git
cd stock-analytics-pipeline
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install yfinance pandas

python fetch.py                 # 1. pull 5y of prices for 20 tickers
python load.py                  # 2. build the SQLite database
python analyze.py               # 3. run SQL analysis
python insights.py              # 4. run pandas analysis
python export_for_tableau.py    # 5. export dashboard-ready data
```

All data is regenerated from source — no data files are committed to the repo.

## What the Analysis Covers

- **Total returns** per ticker over 5 years
- **Daily returns** via `LAG` window function
- **50-day moving averages** via sliding-window aggregation
- **Volatility** per ticker (std dev of daily returns) using a CTE
- **Correlation matrix** of daily returns across all 20 tickers
- **Maximum drawdown** (worst peak-to-trough fall) per ticker
- **Sharpe ratios** (annualized return per unit of risk)

## Key Insights

1. **Small daily edges compound enormously.** NVDA averaged just ~0.24% per
   day — which sounds negligible, but compounded over ~250 trading days per
   year it drove the largest 5-year total return in the group.

2. **Average daily return overstates real growth for volatile stocks.** A
   stock that falls 50% and rises 50% has a 0% average return but a -25%
   actual result. High-volatility names quietly lose to this "volatility
   drag," so returns must be read alongside volatility.

3. **Same-sector stocks offer little diversification.** JPM and BAC daily
   returns correlate at ~0.8 — holding both is closer to one bet than two.
   True diversification requires spreading across sectors, where
   correlations in this dataset drop substantially.

## Dashboard

![Dashboard screenshot](ADD-SCREENSHOT-WHEN-PUBLISHED)

Interactive views: price trends with 50-day moving average overlay, sector
performance comparison, and volatility rankings — filterable by ticker and
date range.

## Roadmap

- [ ] Migrate storage from SQLite to PostgreSQL
- [ ] Schedule daily incremental data refresh
- [ ] Add sector reference table and benchmark comparison vs. S&P 500
- [ ] Move database to AWS RDS and ingestion to Lambda

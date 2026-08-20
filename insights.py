import sqlite3
import pandas as pd

conn = sqlite3.connect("stocks.db")

# pull daily closes out of the database, one column per stock
prices = pd.read_sql("SELECT date, ticker, close FROM daily_prices", conn)
conn.close()

# pivot: rows = dates, columns = tickers (a "wide" table, perfect for math)
wide = prices.pivot(index="date", columns="ticker", values="close")

# daily returns for every stock at once (today / yesterday - 1)
returns = wide.pct_change().dropna()

# --- Experiment 1: who moves together? (correlation) ---
corr = returns.corr()
print("=== Correlation: how much each pair dances together (1 = identical) ===")
# show the 5 tightest pairs (excluding a stock with itself)
pairs = corr.unstack()
pairs = pairs[pairs < 0.999].sort_values(ascending=False)
print("Tightest dance partners:")
print(pairs.head(6).round(2))
print("\nMost independent pairs:")
print(pairs.tail(4).round(2))

# --- Experiment 2: the scariest fall (max drawdown) ---
# for each stock: worst drop from a peak to a valley, in %
running_peak = wide.cummax()
drawdown = (wide / running_peak - 1) * 100
worst = drawdown.min().sort_values()
print("\n=== Worst peak-to-valley fall in 5 years (%) ===")
print(worst.round(1).head(8))

# --- Experiment 3: reward per unit of risk (Sharpe, simplified) ---
sharpe = (returns.mean() / returns.std()) * (252 ** 0.5)  # annualized
print("\n=== Sharpe ratio: return per unit of risk (higher = better deal) ===")
print(sharpe.sort_values(ascending=False).round(2).head(8))
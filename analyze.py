import sqlite3
import pandas as pd

conn = sqlite3.connect("stocks.db")

# make pandas print tables nicely
pd.set_option("display.width", 120)

# --- Question 1: Who won the last 5 years? ---
# For each stock: first price, last price, and total % growth
q1 = """
SELECT
    ticker,
    ROUND(MIN(close), 2) AS lowest_ever,
    ROUND(MAX(close), 2) AS highest_ever,
    ROUND(
        (MAX(CASE WHEN date = (SELECT MAX(date) FROM daily_prices) THEN close END)
        / MAX(CASE WHEN date = (SELECT MIN(date) FROM daily_prices) THEN close END) - 1) * 100
    , 1) AS total_return_pct
FROM daily_prices
GROUP BY ticker
ORDER BY total_return_pct DESC
"""
print("=== Total return over 5 years (the winners) ===")
print(pd.read_sql(q1, conn).head(10))

# --- Question 2: Daily returns (window function #1: LAG) ---
# "How much did each stock move each day compared to yesterday?"
q2 = """
SELECT
    date,
    ticker,
    close,
    ROUND((close / LAG(close) OVER (PARTITION BY ticker ORDER BY date) - 1) * 100, 2)
        AS daily_return_pct
FROM daily_prices
WHERE ticker = 'NVDA'
ORDER BY date DESC
LIMIT 5
"""
print("\n=== NVDA's last 5 daily moves ===")
print(pd.read_sql(q2, conn))

# --- Question 3: 50-day moving average (window function #2: sliding window) ---
q3 = """
SELECT
    date,
    ticker,
    ROUND(close, 2) AS close,
    ROUND(AVG(close) OVER (
        PARTITION BY ticker
        ORDER BY date
        ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_50d
FROM daily_prices
WHERE ticker = 'AAPL'
ORDER BY date DESC
LIMIT 5
"""
print("\n=== AAPL: price vs its 50-day average ===")
print(pd.read_sql(q3, conn))

# --- Question 4: Who's the most jumpy? (CTE + volatility) ---
q4 = """
WITH daily_returns AS (
    SELECT
        ticker,
        (close / LAG(close) OVER (PARTITION BY ticker ORDER BY date) - 1) * 100
            AS ret
    FROM daily_prices
)
SELECT
    ticker,
    ROUND(AVG(ret), 3) AS avg_daily_return,
    ROUND(
        SQRT(AVG(ret * ret) - AVG(ret) * AVG(ret))
    , 2) AS volatility
FROM daily_returns
WHERE ret IS NOT NULL
GROUP BY ticker
ORDER BY volatility DESC
"""
print("\n=== Most jumpy stocks (volatility) ===")
print(pd.read_sql(q4, conn).head(10))

conn.close()
import sqlite3
import pandas as pd

conn = sqlite3.connect("stocks.db")

# one big tidy table: prices + daily return + 50-day moving average
q = """
SELECT
    date,
    ticker,
    close,
    volume,
    (close / LAG(close) OVER (PARTITION BY ticker ORDER BY date) - 1) * 100
        AS daily_return_pct,
    AVG(close) OVER (
        PARTITION BY ticker ORDER BY date
        ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ) AS moving_avg_50d
FROM daily_prices
ORDER BY ticker, date
"""
df = pd.read_sql(q, conn)
conn.close()

df.to_csv("tableau_data.csv", index=False)
print(f"Exported {len(df)} rows to tableau_data.csv")
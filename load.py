import sqlite3
import pandas as pd

# 1. read the CSV we made in step 2
tidy = pd.read_csv("stock_prices.csv")

# make column names database-friendly (lowercase, no spaces)
tidy.columns = [c.lower().replace(" ", "_") for c in tidy.columns]

# 2. open the filing cabinet (creates the file if it doesn't exist)
conn = sqlite3.connect("stocks.db")

# 3. build the drawer: define the table and what goes in it
conn.execute("""
CREATE TABLE IF NOT EXISTS daily_prices (
    date    TEXT,
    ticker  TEXT,
    open    REAL,
    high    REAL,
    low     REAL,
    close   REAL,
    volume  INTEGER
)
""")

# 4. empty the drawer first (so re-running doesn't create duplicates)
conn.execute("DELETE FROM daily_prices")

# 5. pour the data in
tidy[["date", "ticker", "open", "high", "low", "close", "volume"]] \
    .to_sql("daily_prices", conn, if_exists="append", index=False)

conn.commit()

# 6. ask the librarian a question to prove it worked -- your first SQL query!
result = pd.read_sql("""
    SELECT ticker, COUNT(*) AS days, MIN(date) AS first_day, MAX(date) AS last_day
    FROM daily_prices
    GROUP BY ticker
    ORDER BY ticker
""", conn)

print(result)
conn.close()
print("\nDatabase built! You now have a file called stocks.db")
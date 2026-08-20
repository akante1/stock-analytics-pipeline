import yfinance as yf
import pandas as pd

# our basket of stocks - 20 well-known companies across different industries
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",   # tech
    "JPM", "BAC", "V",                          # finance
    "JNJ", "PFE", "UNH",                        # healthcare
    "XOM", "CVX",                               # energy
    "WMT", "COST", "MCD",                       # consumer
    "DIS", "NFLX",                              # media
    "BA", "CAT",                                # industrial
]

print(f"Fetching {len(TICKERS)} stocks... this takes a minute, be patient!")

# grab 5 years of daily prices for ALL of them at once
data = yf.download(TICKERS, period="5y", group_by="ticker")

# reshape it: instead of a super-wide table, make it tall and tidy
# one row = one stock on one day (this shape is what databases love)
all_rows = []
for ticker in TICKERS:
    df = data[ticker].copy()          # take just this stock's columns
    df["ticker"] = ticker             # add a column saying which stock it is
    df = df.reset_index()             # turn the Date from a label into a real column
    all_rows.append(df)

tidy = pd.concat(all_rows)
tidy = tidy.dropna()                  # throw away any empty rows

# save it to a file
tidy.to_csv("stock_prices.csv", index=False)

print(f"Done! Saved {len(tidy)} rows to stock_prices.csv")
print(tidy.head())
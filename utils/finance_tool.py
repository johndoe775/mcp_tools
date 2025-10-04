import pandas as pd
import yfinance as yf
from datetime import datetime



def calculate_price_changes(ticker: str, dod_period: int = 1, wow_period: int = 5, mom_period: int = 22):
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="6mo")
    if stock_data.empty:
        return None

    stock_data = stock_data.reset_index().sort_values(by="Date", ascending=False)

    stock_data["dod"] = stock_data["Close"].pct_change(-dod_period) * 100
    stock_data["wow"] = stock_data["Close"].pct_change(-wow_period) * 100
    stock_data["mom"] = stock_data["Close"].pct_change(-mom_period) * 100

    latest = stock_data[["Date", "Close", "dod", "wow", "mom"]].head(1)
    if latest.empty:
        return None
    row = latest.iloc[0]
    return {
        "Date": row["Date"].isoformat() if isinstance(row["Date"], (pd.Timestamp, datetime)) else str(row["Date"]),
        "Close": None if pd.isna(row["Close"]) else float(row["Close"]),
        "dod": None if pd.isna(row["dod"]) else float(round(row["dod"], 6)),
        "wow": None if pd.isna(row["wow"]) else float(round(row["wow"], 6)),
        "mom": None if pd.isna(row["mom"]) else float(round(row["mom"], 6)),
    }
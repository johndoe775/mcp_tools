import pandas as pd
import yfinance as yf
from datetime import datetime


def get_stock_diffs(ticker: str):
    """
    Returns a DataFrame with the closing price and day‑over‑day (dod %),
    week‑over‑week (wow %) and month‑over‑month (mom %) percentage changes.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., "AAPL").
    periods : list, optional
        List of Yahoo Finance periods to pull. Default is ["5d", "1mo"].
        The first period should contain at least three rows (e.g., "5d")
        so that the three‑period differences can be computed.

    Returns
    -------
    pandas.DataFrame
        Columns: Date, Close, dod %, wow %, mom % (sorted newest‑first).
    """
    periods = ["5d", "1mo"]
    stock = yf.Ticker(ticker)

    # Collect the required rows from each period
    data_frames = []
    for period in periods:
        hist = stock.history(period=period)

        if period == "5d":
            # keep first, second‑last and last rows
            df = hist.iloc[[0, -2, -1]].reset_index()[["Date", "Close"]]
        else:
            # keep only the first row of the longer period
            df = hist.iloc[[0]].reset_index()[["Date", "Close"]]

        data_frames.append(df)

    # Combine the slices
    result_df = pd.concat(data_frames, ignore_index=True)

    # Sort by date descending
    result_df = result_df.sort_values("Date", ascending=False)

    # Keep only the date part (drop timezone / time)
    result_df["Date"] = result_df["Date"].dt.date

    # Percentage differences
    result_df["dod %"] = result_df["Close"].diff(-1) / result_df["Close"].shift(-1) * 100
    result_df["wow %"] = result_df["Close"].diff(-2) / result_df["Close"].shift(-2) * 100
    result_df["mom %"] = result_df["Close"].diff(-3) / result_df["Close"].shift(-3) * 100

    # Remove rows where any diff is NaN (the earliest rows)
    result_df.dropna(inplace=True)

    # Re‑order columns for readability
    result_df= result_df[["Date", "Close", "dod %", "wow %", "mom %"]]
    result_df["Date"] = result_df["Date"].astype(str)
    columns=result_df.columns
    values=result_df.values[0]
    result=dict()
    for i,j in zip(columns, values):
        result[i]=j

    return result
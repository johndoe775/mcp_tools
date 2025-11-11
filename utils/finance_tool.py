import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from sklearn.linear_model import LinearRegression


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
    result_df["dod %"] = (
        result_df["Close"].diff(-1) / result_df["Close"].shift(-1) * 100
    )
    result_df["wow %"] = (
        result_df["Close"].diff(-2) / result_df["Close"].shift(-2) * 100
    )
    result_df["mom %"] = (
        result_df["Close"].diff(-3) / result_df["Close"].shift(-3) * 100
    )

    # Remove rows where any diff is NaN (the earliest rows)
    result_df.dropna(inplace=True)

    # Re‑order columns for readability
    result_df = result_df[["Date", "Close", "dod %", "wow %", "mom %"]]
    result_df["Date"] = result_df["Date"].astype(str)
    columns = result_df.columns
    values = result_df.values[0]
    result = dict()
    for i, j in zip(columns, values):
        result[i] = j

    return result


def calculate_correlation(ticker1, ticker2):
    """
    Calculate the correlation between the given stock ticker and another ticker.

    Parameters
    ----------
    ticker1 : str
        The first stock ticker symbol.
    ticker2 : str
        The second stock ticker symbol.

    Returns
    -------
    float
        The correlation between the two tickers.
    """
    stock1 = yf.download(ticker1, period="6mo")
    stock2 = yf.download(ticker2, period="6mo")

    stock1_close = stock1["Close"].pct_change().dropna()
    stock2_close = stock2["Close"].pct_change().dropna()

    common_dates = stock1_close.index.intersection(stock2_close.index)
    stock1_close = stock1_close.loc[common_dates]
    stock2_close = stock2_close.loc[common_dates]

    correlation = (
        stock1_close.reset_index()
        .iloc[:, -1]
        .corr(stock2_close.reset_index().iloc[:, -1])
    )
    return correlation


def get_alpha_beta_OLS(ticker, period="6mo"):
    """
    Calculate annualized alpha and beta for a given ticker vs Nifty 50 (^NSEI) using sklearn LinearRegression.
    period: '6mo' or '1y'.
    Returns: dict {'alpha': annual_alpha (float), 'beta': beta (float)}.
    Raises ValueError on bad inputs or insufficient data.
    """
    if period not in ("6mo", "1y"):
        raise ValueError("period must be '6mo' or '1y'")

    index_ticker = "^NSEI"
    asset = yf.Ticker(ticker)
    index = yf.Ticker(index_ticker)

    hist_asset = asset.history(period=period)
    hist_index = index.history(period=period)

    if hist_asset.empty or hist_index.empty:
        raise ValueError("No historical data returned for asset or index.")

    if "Close" not in hist_asset.columns or "Close" not in hist_index.columns:
        raise ValueError("Downloaded data missing 'Close' column.")

    common_dates = hist_asset.index.intersection(hist_index.index)
    if len(common_dates) < 2:
        raise ValueError("Not enough overlapping data points between asset and index.")

    asset_prices = hist_asset.loc[common_dates, "Close"]
    index_prices = hist_index.loc[common_dates, "Close"]

    asset_ret = asset_prices.pct_change().dropna()
    index_ret = index_prices.pct_change().dropna()

    common_dates = asset_ret.index.intersection(index_ret.index)
    asset_ret = asset_ret.loc[common_dates]
    index_ret = index_ret.loc[common_dates]

    if len(asset_ret) < 10:
        raise ValueError(
            "Insufficient return observations after alignment (need >=10)."
        )

    # Prepare X and y for sklearn (reshape X to 2D)
    X = index_ret.values.reshape(-1, 1)
    y = asset_ret.values

    model = LinearRegression().fit(X, y)
    beta = float(model.coef_[0])
    # Intercept is daily alpha (asset return = intercept + beta * index return)
    daily_alpha = float(model.intercept_)
    annual_alpha =  (1 + daily_alpha) ** len(common_dates) - 1

    return {"alpha": annual_alpha, "beta": beta}

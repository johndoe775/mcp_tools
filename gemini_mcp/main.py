from fastmcp import FastMCP
from typing import Optional
import logging
import sys
import os

sys.path.append( '..')

from utils.finance_tool import get_stock_diffs, calculate_correlation, get_alpha_beta_OLS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_price_tool")

mcp = FastMCP("Price MCP Server")


@mcp.tool
def price_get(ticker: str):
    """
    MCP tool wrapper for calculate_price_changes.

    Args:
      ticker: stock ticker string
      dod: day-over-day period (int)
      wow: week-over-week period (int)
      mom: month-over-month period (int)

    Returns:
      dict with keys: Date, Close, dod, wow, mom OR {"error": "..."}
    """
    try:
        if not ticker or not isinstance(ticker, str):
            return {"error": "ticker (str) is required"}
        result = get_stock_diffs(ticker)
    except Exception as e:
        logger.exception("Error in price_get")
        return {"error": str(e)}

    if result is None:
        return {"error": f"No data for ticker {ticker}"}
    return result


@mcp.tool
def correlation(ticker1: str, ticker2: str):
    """
    MCP tool wrapper for calculate_correlation.

    Args:
      ticker1: first stock ticker string
      ticker2: second stock ticker string

    Returns:
      correlation coefficient between the two tickers OR {"error": "..."}
    """
    try:
        if (
            not ticker1
            or not isinstance(ticker1, str)
            or not ticker2
            or not isinstance(ticker2, str)
        ):
            return {"error": "Both ticker1 (str) and ticker2 (str) are required"}
        result = calculate_correlation(ticker1, ticker2)
    except Exception as e:
        logger.exception("Error in correlation")
        return {"error": str(e)}

    if result is None:
        return {"error": f"Failed to calculate correlation for {ticker1} and {ticker2}"}
    return {"correlation": result}


@mcp.tool
def alpha_beta_get(ticker: str, period: str = "6mo"):
    """
    MCP tool: Calculate annualized alpha & beta for a ticker vs Nifty 50 ('^NSEI').
    Args:
      ticker: stock ticker string (e.g. 'RELIANCE.NS')
      period: '6mo' or '1y'
    Returns:
      dict: {'alpha': ..., 'beta': ...} or {'error': ...}
    """
    try:
        if not ticker or not isinstance(ticker, str):
            return {"error": "ticker (str) is required"}
        if period not in ("6mo", "1y"):
            return {"error": "period must be '6mo' or '1y'"}
        result = get_alpha_beta_OLS(ticker, period)
    except Exception as e:
        return {"error": str(e)}
    if result is None:
        return {"error": f"Could not compute alpha/beta for ticker {ticker}"}
    return result


if __name__ == "__main__":
    # run over HTTP on port 8000 to match your examples
    mcp.run(transport="stdio")

from fastmcp import FastMCP
from typing import Optional
import logging
from utils.finance_tool import get_stock_diffs
from utils.hr_tool import prompt_selection



mcp = FastMCP("Multi Tool Server")


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
        
        return {"error": str(e)}

    if result is None:
        return {"error": f"No data for ticker {ticker}"}
    return result


@mcp.tool
def prompt_selector(conv: str):
    """
    based on the input given select the appropriate prompt and return the prompt name


    """
    try:
        name = prompt_selection(conv)
        return name
    except Exception as e:
        return e


if __name__ == "__main__":
    # run over HTTP on port 8000 to match your examples
    mcp.run(transport="http",port=8000)

from fastmcp import FastMCP
from typing import Optional
import logging
from utils.finance_tool import calculate_price_changes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_price_tool")

mcp = FastMCP("Price MCP Server")


@mcp.tool
def price_get(
    ticker: str, dod: Optional[int] = 1, wow: Optional[int] = 5, mom: Optional[int] = 22
):
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
        result = calculate_price_changes(ticker, int(dod), int(wow), int(mom))
    except Exception as e:
        logger.exception("Error in price_get")
        return {"error": str(e)}

    if result is None:
        return {"error": f"No data for ticker {ticker}"}
    return result


if __name__ == "__main__":
    # run over HTTP on port 8000 to match your examples
    mcp.run(transport="stdio")

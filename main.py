from fastmcp import FastMCP
from typing import Optional
import logging
from utils.finance_tool import get_stock_diffs
from advanced_rag_tools import sql_tool
from advanced_rag_tools.state import GraphState

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
def pandasql_tool(state: GraphState):
    """
    use this tool for generating sql queries on pandas dataframe

    """
    try:
        result = pandasql_tool(state)
        state["message"].append("completed pandas visualization")
        return state
    except Exception as e:
        state["message"].append(f"error {e}")
        return state


if __name__ == "__main__":
    # run over HTTP on port 8000 to match your examples
    mcp.run(transport="stdio")

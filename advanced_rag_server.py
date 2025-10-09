from fastmcp import FastMCP
from typing import Optional
import logging
from advanced_rag_tools.sql_tool import pandasql_tool
from advanced_rag_tools.state import GraphState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_price_tool")

mcp = FastMCP("Advanced RAG MCP Server")


@mcp.tool
def pandas_sql_tool(state: GraphState):
    """

    This tool accepts a natural language description of the desired data operation,
    processes the input entirely within the tool, and generates the corresponding
    SQL query to be executed against a pandas DataFrame. The natural language input
    is interpreted to formulate appropriate SELECT, WHERE, GROUP BY, and other SQL
    clauses, enabling seamless conversion from plain English to executable queries.
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

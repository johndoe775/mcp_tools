from fastmcp import FastMCP
from typing import Optional
import logging
from advanced_rag_tools.sql_tool import pandasql_tool
from advanced_rag_tools.state import GraphState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pandas_sql_tool")

mcp = FastMCP("Advanced RAG MCP Server")


@mcp.tool
def pandas_sql_tool(state: GraphState):
    """
    This tool accepts a natural language description of the desired data operation and creates an inputs that shall be used with state to run thr pandasql_tool.

    """

    try:
        result = pandasql_tool(state["inputs"])

        return state

    except Exception as e:
        state["messages"].append(f"error {e}")
        return state


if __name__ == "__main__":
    # run over HTTP on port 8000 to match your examples
    mcp.run(transport="stdio")

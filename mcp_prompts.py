import sys
import os
from fastmcp import FastMCP


def main():
    # Get YAML prompt file path from environment or CLI argument
    prompt_file = os.environ.get("MCP_PROMPT_PATH") or (
        sys.argv[1] if len(sys.argv) > 1 else "/workspaces/mcp_tools/src/prompts.yaml"
    )

    # Initialize the MCP server with the given YAML prompt configuration
    mcp = FastMCP(name="ResumeToolsServer", config_path=prompt_file)

    mcp.run(
        transport="stdio"
    )  # Start the server (defaults to stdio for tools like Claude Desktop)


if __name__ == "__main__":
    main()

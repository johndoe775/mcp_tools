import sys
import os
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP(name="ResumeToolsServer")

# Get YAML prompt file path from environment or CLI argument
prompt_file = os.environ.get("MCP_PROMPT_PATH") or (
    sys.argv[1] if len(sys.argv) > 1 else "/workspaces/mcp_tools/src/prompts.yaml"
)


# Load tools from the YAML prompt configuration using the decorator
@mcp.prompt(prompt_file)
def load_prompts_from_yaml():
    """This function is a placeholder for the @mcp.prompts decorator."""
    pass


def main():
    """Runs the MCP server."""
    mcp.run(
        transport="stdio"
    )  # Start the server (defaults to stdio for tools like Claude Desktop)


if __name__ == "__main__":
    main()

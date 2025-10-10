import json
import asyncio
from fastmcp import Client


async def main() -> None:
    server_script = "main.py"

    # use the client's async context manager so it connects properly
    async with Client(server_script) as client:
        print([i.name for i in await client.list_tools()])

        ticker = "AAPL"
        try:
            result = await client.call_tool("price_get", {"ticker": ticker})
            print(f"Result: {result.content[0].text}")

        except Exception as exc:
            print(f"Error calling tool: {exc}")
            return


if __name__ == "__main__":
    asyncio.run(main())

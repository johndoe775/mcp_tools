import streamlit as st
import asyncio
from fastmcp import Client
import json


async def get_price(ticker):
    server_script = "main.py"
    async with Client(server_script) as client:
        try:
            result = await client.call_tool("price_get", {"ticker": ticker})
            return result.content[0].text
        except Exception as exc:
            return f"Error: {exc}"


def main():
    st.title("Stock Price Checker")
    ticker = st.text_input("Enter stock ticker", value="AAPL")
    if st.button("Get Price"):

        result = asyncio.run(get_price(ticker))
        try:
            st.write(f"Current price of {ticker}:")
            st.code(json.dumps({"price": result}, indent=4), language="json")
        except Exception as exc:
            st.write(f"Error: {exc}")


if __name__ == "__main__":
    main()

from typing import List, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import PromptTemplate
from research.helpers import LLM

# from research.tools import pandas_tool, sql_tool
import argparse


# Replace with the actual LLM library you're using
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        messages: A list of messages exchanged in the conversation.
        inputs: The current user input.
    """

    messages: Annotated[List, add_messages]
    inputs: str
    choice: str
    answer: str
    tool_choice: str  # Store the tool choice for the ToolNode

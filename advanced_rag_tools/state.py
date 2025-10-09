from typing import List, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        messages: A list of messages exchanged in the conversation.
        inputs: The current user input.
    """

    messages: Annotated[List, add_messages]
    inputs: str

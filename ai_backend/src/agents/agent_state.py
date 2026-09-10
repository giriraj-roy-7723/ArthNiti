from typing import Annotated, TypedDict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class BusinessAgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    image_url: Optional[str]
    image_base64: Optional[str]
    vision_context: Optional[str]

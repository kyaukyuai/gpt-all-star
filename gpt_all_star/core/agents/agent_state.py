import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages.base import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

from typing import TypedDict, List, Annotated
from langchain_core.messages import HumanMessage,BaseMessage
import operator

class ResearchAgentState(TypedDict):
    user_input: HumanMessage
    plan: str | None = None
    writer_messages: Annotated[List[BaseMessage],operator.add] | None = None
    draft : str | None = None
    need_improve:bool = False
    notes: str | None = None
    current_tries:int = 0
    max_tries : int = 2
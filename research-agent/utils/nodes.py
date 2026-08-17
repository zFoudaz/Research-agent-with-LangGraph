from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage
from langgraph.prebuilt import ToolNode
from .tools import search
from dotenv import load_dotenv
load_dotenv()
import os
from .state import ResearchAgentState
from .schemas import reviewerSchema
from .prompts import PLANNER_SYSTEM_PROMPT, WRITER_SYSTEM_PROMPT, REVIEWER_SYSTEM_PROMPT, WRITER_IMPROVE_SYSTEM_PROMPT

llm = AzureChatOpenAI(
    api_key= os.environ['OPENAI_KEY'],
    model='gpt-4.1-mini',
    azure_endpoint= os.environ['OPENAI_BASE_URL'],
    api_version='2024-12-01-preview'
)
# ================= planer Node =================
def planner(state:ResearchAgentState) -> ResearchAgentState:
    user_input = state['user_input']
    response = llm.invoke([SystemMessage(content=PLANNER_SYSTEM_PROMPT)] + [user_input])
    return {
        'plan':response.content
    }

# ================= Writer Node and Tools =================
#tool node
writer_tools = [search]
writer_tools_node = ToolNode(writer_tools, messages_key='writer_messages')
#node
def writer(state:ResearchAgentState) -> ResearchAgentState:
    writer_llm = llm.bind_tools(writer_tools)
    if state['need_improve']:
        state['need_improve']=False
        state['writer_messages'] = None
        llm_input = f"research to improve: \n {state['draft']}\n\n notes to follow: {state['notes']}"
        state['writer_messages'].append(SystemMessage(content = WRITER_IMPROVE_SYSTEM_PROMPT + llm_input))
    if not state['writer_messages']:
        topic = state['user_input'].content
        plan = state['plan']
        llm_input = f"topic: {topic}\n the plan to follow:\n {plan}"
        state['writer_messages'].append(SystemMessage(content = WRITER_SYSTEM_PROMPT + llm_input))
    msg = writer_llm.invoke(state['writer_messages'])
    return {
        'need_improve':state['need_improve'],
        'draft':msg.content,
        'writer_messages':[msg]
    }
# conditional edge function
def is_tool_called(state:ResearchAgentState) -> str :
    last_message = state['writer_messages'][-1]
    if not last_message.tool_call:
        return 'Finished'
    else:
        return "toolCalled"

# ================= Reviewer Node =================

def reviewer(state:ResearchAgentState) -> ResearchAgentState:
    draft = state['draft']
    structured_output = llm.with_structured_output(reviewerSchema)
    review = structured_output.invoke([SystemMessage(content=REVIEWER_SYSTEM_PROMPT)] + [HumanMessage(content=draft)])
    return review
# conditional edge function
def needs_improve(state:ResearchAgentState) -> bool:
    if state['need_improve']:
        return 'NeedsImprove'
    else:
        return 'Good'
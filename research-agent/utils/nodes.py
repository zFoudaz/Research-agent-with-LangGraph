from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage
from langchain.agents import create_agent
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
        'plan':response.content,
        'current_tries':0
    }

# ================= Writer Node and Tools =================
#tool node
writer_tools = [search]
writer_agent = create_agent(llm,tools=writer_tools)
#node
def writer(state:ResearchAgentState) -> ResearchAgentState:
    if state.get('need_improve'):
        llm_input = f"research to improve: \n{state['draft']}\n\n notes to follow: {state['notes']}"
        system_prompt = WRITER_IMPROVE_SYSTEM_PROMPT + llm_input
    else:
        topic = state['user_input'].content
        plan = state['plan']
        llm_input = f"topic: {topic}\nthe plan to follow:\n{plan}"
        system_prompt = WRITER_SYSTEM_PROMPT + llm_input
    result = writer_agent.invoke({
        'messages':[SystemMessage(content=system_prompt)]
    })
    final_msg = result['messages'][-1]

    return{
        'need_improve':False,
        'draft':final_msg.content,
        'current_tries':state['current_tries']+1
    }


# ================= Reviewer Node =================

def reviewer(state:ResearchAgentState) -> ResearchAgentState:
    draft = state['draft']
    structured_output = llm.with_structured_output(reviewerSchema)
    review = structured_output.invoke([SystemMessage(content=REVIEWER_SYSTEM_PROMPT)] + [HumanMessage(content=draft)])
    return review
# conditional edge function
def needs_improve(state:ResearchAgentState) -> bool:
    if state['need_improve'] and state['current_tries'] < state['max_tries']:
        return 'NeedsImprove'
    else:
        return 'Good'
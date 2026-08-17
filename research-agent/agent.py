from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from utils.state import ResearchAgentState
from utils.nodes import planner, writer, reviewer # nodes
from utils.nodes import  needs_improve # conditional edges

builder = StateGraph(ResearchAgentState)
builder.add_node('planner',planner)
builder.add_node('writer',writer)
builder.add_node('reviewer',reviewer)

builder.add_edge(START,'planner')
builder.add_edge('planner','writer')
builder.add_edge('writer','reviewer')

builder.add_conditional_edges('reviewer',needs_improve,{'NeedsImprove':'writer','Good':END})

research_agent = builder.compile()

doc = research_agent.invoke({
    'user_input':HumanMessage(content='what is MCP or Model context protocol?'),
    'need_improve':False,
    'max_tries':3
})

print(doc)


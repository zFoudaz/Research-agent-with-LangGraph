from langgraph.graph import StateGraph, START, END
from utils.state import ResearchAgentState
from utils.nodes import planner, writer, writer_tools_node, reviewer # nodes
from utils.nodes import is_tool_called, needs_improve # conditional edges

builder = StateGraph(ResearchAgentState)
builder.add_node('planner',planner)
builder.add_node('writer',writer)
builder.add_node('writer tools',writer_tools_node)
builder.add_node('reviewer',reviewer)

builder.add_edge(START,'planner')
builder.add_edge('planner','writer')
builder.add_edge('writer tools','writer')

builder.add_conditional_edges('writer',is_tool_called,{'toolCalled':'writer tools','Finished':'reviewer'})
builder.add_conditional_edges('reviewer',needs_improve,{'NeedsImprove':'writer','Good':END})

research_agent = builder.compile()


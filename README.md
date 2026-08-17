# Research Agent with LangGraph

An agentic research workflow built with LangGraph, LangChain, Azure OpenAI, and Tavily search. It follows a simple loop:

1. A planner turns the user topic into a research plan.
2. A writer drafts the research using internet search when needed.
3. A reviewer checks the draft and either approves it or sends it back for improvement.

## Features

- Multi-step research pipeline with LangGraph
- Internet search through Tavily
- Azure OpenAI-backed planning, drafting, and review 
    note: you can change the llm from  `research-agent/utils/nodes.py` if you have openAI API key
- Iterative rewrite loop when the reviewer requests improvements

## Project Structure

```text
research-agent/
  agent.py
  utils/
    nodes.py
    prompts.py
    schemas.py
    state.py
    tools.py
```

## Graph View

The agent flow is visualized here:

![Research agent graph](Agent%20Graph.png)

## Requirements

- Python 3.10+ recommended
- An Azure OpenAI account and deployment access
- A Tavily API key

## Environment Variables

Create a `.env` file in the project root with:

```env
OPENAI_KEY=your_azure_openai_api_key
OPENAI_BASE_URL=your_azure_openai_endpoint
TAVILY_API_KEY=your_tavily_api_key
```

You can also start from `.env.example`.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

The current entry point is `research-agent/agent.py`:

```bash
python research-agent/agent.py
```

The script currently invokes the agent with a built-in example prompt:

```python
tell me about the history of Egypt
```

## How It Works

- `planner` builds a research plan from the user input.
- `writer` produces a draft and can use the Tavily search tool.
- `reviewer` evaluates the draft and returns improvement notes when needed.
- The graph loops back to `writer` until the draft is accepted or the retry limit is reached.

## Notes

- The Azure model is configured in `research-agent/utils/nodes.py`.
- The retry limit is controlled by `max_tries` in the agent state.
- The script prints the final graph output to the console.

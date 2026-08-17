from langchain_core.tools import tool
from tavily import TavilyClient
from typing import List
import os


@tool 
def search(query:str) -> List[str]:
    """
    a tool uses tavily search that takes query and returns results from the internet 
    Args:
        query : the query to get research results 
    Returns: 
        result: list of related documents
    """

    tavily_client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'] )
    response = tavily_client.search(query,max_results=2)

    return response['results']

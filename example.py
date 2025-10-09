from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from typing import Any, Dict, List

load_dotenv()
mcp= FastMCP("web_search", host="0.0.0.0", port=8000)

if "TAVILY_API_KEY" not in os.environ:
    raise Exception("TAVILY_API_KEY envirnment variable not set")

TAVILY_API_KEY= os.getenv("TAVILY_API_KEY")
    
tavily_client= TavilyClient(TAVILY_API_KEY)

@mcp.tool()
def web_search(query: str) -> List[Dict]:
    """Use this tool to search the web for information.

    Args:
        query (str): The search query.
         
    Returns:
        List[Dict]: The search results.
    """
    try:
        response= tavily_client.search(query)
        return response["results"]
    
    except:
       return "No results found"
   
   
   # Run the server
if __name__ == "__main__":
    print("Server has started on http://0.0.0.0:8000")
    mcp.run(transport="streamable-http")
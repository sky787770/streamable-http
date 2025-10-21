from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from typing import Any, Dict, List
from datetime import datetime

load_dotenv()

mcp = FastMCP("web_search", host="0.0.0.0", port=8000)

if "TAVILY_API_KEY" not in os.environ:
    raise Exception("TAVILY_API_KEY environment variable not set")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
tavily_client = TavilyClient(TAVILY_API_KEY)

@mcp.tool()
def web_search(query: str) -> List[Dict]:
    """Use this tool to search the web for information.

    Args:
        query (str): The search query.
         
    Returns:
        List[Dict]: The search results.
    """
    try:
        response = tavily_client.search(query)
        return response["results"]
    
    except Exception as e:
       return f"Error: {str(e)}"

@mcp.tool()
def current_time(Zone: str = "Asia/Kolkata"):
    """Use this tool to find current/today's time information.
    Args: 
      Zone(str): Resion for which we want to find current_time.
    Returns:
       current datetime
    """
    return datetime.now()

# Run the server
if __name__ == "__main__":
    from fastapi.middleware.cors import CORSMiddleware
    
    # Access the internal FastAPI app
    if hasattr(mcp, '_app'):
        mcp._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    print("Server has started on http://0.0.0.0:8000")
    mcp.run(transport="streamable-http")

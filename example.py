from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from typing import Any, Dict, List

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
    
    except:
       return "No results found"

# Run the server
if __name__ == "__main__":
    import uvicorn
    from fastapi.middleware.cors import CORSMiddleware
    
    # Get the FastAPI app from FastMCP
    app = mcp.get_app()
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
    )
    
    print("Server has started on http://0.0.0.0:8000")
    
    # Run with uvicorn directly
    uvicorn.run(app, host="0.0.0.0", port=8000)

from tavily import TavilyClient
from typing import List
from .models import WebSearchResult
import os

def search_web(query: str, api_key: str = None) -> List[WebSearchResult]:
    if not api_key:
        api_key = os.getenv("TAVILY_API_KEY")
    client = TavilyClient(api_key=api_key)
    results = client.search(query=query, search_depth="advanced")
    web_results = []
    for result in results["results"]:
        web_result = WebSearchResult(
            title=result["title"],
            content=result["content"],
            url=result["url"],
            metadata={"score": result.get("score", 0)}
        )
        web_results.append(web_result)
    return web_results
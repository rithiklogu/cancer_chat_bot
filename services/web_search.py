import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

@tool
def search_web_tool(query: str) -> dict:
    """
    Searches the web for cancer-related content using SerpAPI.
    Returns the top result with title, snippet, and link.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    params = {
        "q": query,
        "api_key": os.getenv("SERP_API_KEY"),
        "engine": "google"
    }

    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code != 200:
        raise Exception(f"Search API failed: {response.status_code} - {response.text}")

    results = response.json().get("organic_results", [])
    if not results:
        return {"error": "No results found."}

    top_result = results[0]
    return {
        "title": top_result.get("title"),
        "snippet": top_result.get("snippet"),
        "link": top_result.get("link")
    }

# result = search_web_tool("what is cancer")
# print(result)
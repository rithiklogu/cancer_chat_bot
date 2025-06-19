import os
import requests
from dotenv import load_dotenv 

load_dotenv()

def search_web(query: str):
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

    return [f"{res.get('title')} - {res.get('snippet')}" for res in results[:5]]




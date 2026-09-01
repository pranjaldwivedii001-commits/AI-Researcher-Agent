from langchain.tools import tool
import requests
import os
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()
from rich import print


tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) ->str :
    "Search the web for recent and reliable information on a topic . Returns Titles, url, snippet"
    results = tavily.search(query = query, max_result=4)

    out=[]
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\n URL: {r['url']}\nSnippet:{r['content'][0:50]}\n"
        )
    return "\n..\n".join(out)


@tool
def scrape_webpage(url: str) -> str:
    """Scrape text content from a given URL to use for research and gathering information."""
    try:
        # Use headers to mimic a real browser request and avoid 403 blocks
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/115.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes (404, 500, etc.)

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove boilerplate/noise elements to keep only relevant text
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        # Extract all visible text cleanly
        text = soup.get_text(separator="\n", strip=True)

        # Truncate text if it's too massive to protect your LLM token limit (e.g., ~10,000 characters)
        max_chars = 3000
        if len(text) > max_chars:
            return text[:max_chars] + "\n[Content truncated due to length...]"
            
        return text

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve URL due to network error: {str(e)}"
    except Exception as e:
        return f"An error occurred while parsing the webpage: {str(e)}"


    
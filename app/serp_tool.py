from dotenv import load_dotenv
from tavily import TavilyClient
import os

load_dotenv()

# create once better performance
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def serp_answer(question):
    result = client.search(query=question, max_results=3)

    return "Search results:\n\n" + "\n\n".join(
        f"Title: {item['title']}\nURL: {item['url']}\nContent: {item['content']}"
        for item in result.get("results", [])
    )
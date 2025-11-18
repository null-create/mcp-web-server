"""
Web Search MCP Server
A comprehensive web search server using multiple backends without API keys.
"""

import os
import logging
from typing import Any, Dict

from fastmcp import FastMCP
from search_backends import SearchBackends

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST_PORT = int(os.getenv("HOST_PORT", "9393"))
HOST_ADDRESS = os.getenv("HOST_ADDRESS", "0.0.0.0")

# Initialize the FastMCP server
mcp = FastMCP("Web Search Server", host=HOST_ADDRESS, port=HOST_PORT)

# Initialize search backends
search_backends = SearchBackends()


@mcp.tool(name="web_search", description="Search the web using DuckDuckGo")
def web_search(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
    safesearch: str = "moderate",
) -> Dict[str, Any]:
    """
    Search the web.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (1-50)
        region: Search region code (e.g., us-en, uk-en, wt-wt for worldwide)
        safesearch: Safe search setting (strict, moderate, off)

    Returns:
        Dictionary containing search results with titles, URLs, and snippets
    """
    try:
        max_results = max(1, min(50, max_results))
        results = search_backends.search_duckduckgo(
            query, max_results, region, safesearch
        )

        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": results,
        }

    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


@mcp.tool(name="news_search", description="Search for news articles.")
def news_search(
    query: str, max_results: int = 10, region: str = "wt-wt", time_range: str = "d"
) -> Dict[str, Any]:
    """
    Search for news articles using DuckDuckGo news search.

    Args:
        query: News search query
        max_results: Maximum number of news articles to return (1-30)
        region: Search region code
        time_range: Time range for news (d=day, w=week, m=month, y=year)

    Returns:
        Dictionary containing news articles with titles, URLs, dates, and sources
    """
    try:
        max_results = max(1, min(30, max_results))
        results = search_backends.search_news(query, max_results, region, time_range)

        return {
            "success": True,
            "query": query,
            "time_range": time_range,
            "results_count": len(results),
            "results": results,
        }

    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


@mcp.tool(name="image_search", description="Search for images.")
def image_search(
    query: str,
    max_results: int = 10,
    size: str = "Medium",
    type_image: str = "photo",
    region: str = "wt-wt",
) -> Dict[str, Any]:
    """
    Search for images using DuckDuckGo image search.

    Args:
        query: Image search query
        max_results: Maximum number of images to return (1-50)
        size: Image size (Small, Medium, Large, Wallpaper)
        type_image: Image type (photo, clipart, gif, transparent, line)
        region: Search region code

    Returns:
        Dictionary containing image URLs, titles, and sources
    """
    try:
        max_results = max(1, min(50, max_results))
        results = search_backends.search_images(
            query, max_results, size, type_image, region
        )

        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": results,
        }

    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


@mcp.tool(name="video_search", description="Search for videos.")
def video_search(
    query: str,
    max_results: int = 10,
    duration: str = "Medium",
    resolution: str = "High",
    region: str = "wt-wt",
) -> Dict[str, Any]:
    """
    Search for videos using DuckDuckGo video search.

    Args:
        query: Video search query
        max_results: Maximum number of videos to return (1-50)
        duration: Video duration (Short, Medium, Long)
        resolution: Video resolution (High, Standard)
        region: Search region code

    Returns:
        Dictionary containing video URLs, titles, durations, and sources
    """
    try:
        max_results = max(1, min(50, max_results))
        results = search_backends.search_videos(
            query, max_results, duration, resolution, region
        )

        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": results,
        }

    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


@mcp.tool(name="search_wikipedia", description="Search wikipedia for related articles")
def search_wikipedia(query: str) -> list[Dict[str, Any]]:
    """
    Search wikipedia.
    """
    try:
        max_results = max(1, min(50, max_results))
        results = search_backends.search_wikipedia(query, max_results)

        return {
            "success": True,
            "query": query,
            "result_count": len(results),
            "results": results,
        }
    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


@mcp.tool(name="search_github", description="Search github")
def search_github(query: str, max_results: int = 10) -> list[Dict[str, Any]]:
    """Search github for related projects"""
    try:
        max_results = max(1, min(50, max_results))
        results = search_backends.search_github(query)

        return {
            "success": True,
            "query": query,
            "result_count": len(results),
            "results": results,
        }
    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


@mcp.tool(name="get_search_suggestions", description="Get search suggestions.")
def get_search_suggestions(query: str, region: str = "wt-wt") -> Dict[str, Any]:
    """
    Get search suggestions for a query using DuckDuckGo.

    Args:
        query: Partial search query to get suggestions for
        region: Search region code

    Returns:
        Dictionary containing search suggestions
    """
    try:
        suggestions = search_backends.get_suggestions(query, region)

        return {
            "success": True,
            "query": query,
            "suggestions_count": len(suggestions),
            "suggestions": suggestions,
        }

    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


if __name__ == "__main__":
    try:
        mcp.run(transport="http")
    except KeyboardInterrupt:
        print("Shutting down the Web Search MCP Server...")

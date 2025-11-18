"""
Search backend implementations for the web search MCP server.
Uses various libraries that don't require API keys.
"""

import requests
from typing import Any, Dict, List

from ddgs import DDGS
import wikipedia


class SearchBackends:
    """Handles various search backends without requiring API keys."""

    def __init__(
        self,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ):
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.user_agent,
            }
        )

    def search_duckduckgo(
        self,
        query: str,
        max_results: int = 10,
        region: str = "wt-wt",
        safesearch: str = "moderate",
    ) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = []
                search_results = ddgs.text(
                    query=query,
                    region=region,
                    safesearch=safesearch,
                    max_results=max_results,
                )

                for result in search_results:
                    results.append(
                        {
                            "title": result.get("title", ""),
                            "url": result.get("href", ""),
                            "snippet": result.get("body", ""),
                            "source": "DuckDuckGo",
                        }
                    )

                return results[:max_results]

        except Exception as e:
            raise Exception(f"DuckDuckGo search failed: {str(e)}")

    def search_news(
        self,
        query: str,
        max_results: int = 10,
        region: str = "wt-wt",
        time_range: str = "d",
    ) -> List[Dict[str, Any]]:
        """Search news using DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = []
                news_results = ddgs.news(
                    query=query,
                    region=region,
                    timelimit=time_range,
                    max_results=max_results,
                )

                for result in news_results:
                    results.append(
                        {
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "snippet": result.get("body", ""),
                            "date": result.get("date", ""),
                            "source": result.get("source", "DuckDuckGo News"),
                        }
                    )

                return results[:max_results]

        except Exception as e:
            raise Exception(f"DuckDuckGo news search failed: {str(e)}")

    def search_images(
        self,
        query: str,
        max_results: int = 10,
        size: str = "Medium",
        type_image: str = "photo",
        region: str = "wt-wt",
    ) -> List[Dict[str, Any]]:
        """Search images using DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = []
                image_results = ddgs.images(
                    query=query,
                    region=region,
                    size=size,
                    type_image=type_image,
                    max_results=max_results,
                )

                for result in image_results:
                    results.append(
                        {
                            "title": result.get("title", ""),
                            "url": result.get("image", ""),
                            "thumbnail": result.get("thumbnail", ""),
                            "source": result.get("source", "DuckDuckGo Images"),
                            "width": result.get("width", ""),
                            "height": result.get("height", ""),
                        }
                    )

                return results[:max_results]

        except Exception as e:
            raise Exception(f"DuckDuckGo image search failed: {str(e)}")

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        duration: str = "Medium",
        resolution: str = "High",
        region: str = "wt-wt",
    ) -> List[Dict[str, Any]]:
        """Search videos using DuckDuckGo."""
        if not DDGS:
            raise ImportError(
                "duckduckgo-search library not available. Install with: pip install duckduckgo-search"
            )

        try:
            with DDGS() as ddgs:
                results = []
                video_results = ddgs.videos(
                    query=query,
                    region=region,
                    duration=duration,
                    resolution=resolution,
                    max_results=max_results,
                )

                for result in video_results:
                    results.append(
                        {
                            "title": result.get("title", ""),
                            "url": result.get("content", ""),
                            "thumbnail": result.get("image", ""),
                            "duration": result.get("duration", ""),
                            "source": result.get("publisher", "DuckDuckGo Videos"),
                            "published": result.get("published", ""),
                        }
                    )

                return results[:max_results]

        except Exception as e:
            raise Exception(f"DuckDuckGo video search failed: {str(e)}")

    def get_suggestions(self, query: str, region: str = "wt-wt") -> List[str]:
        """Get search suggestions using DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                suggestions = ddgs.suggestions(query=query, region=region)
                return [s.get("phrase", "") for s in suggestions if s.get("phrase")]

        except Exception as e:
            raise Exception(f"DuckDuckGo suggestions failed: {str(e)}")

    def search_wikipedia(
        self, query: str, max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Search Wikipedia."""
        try:
            results = []
            search_results = wikipedia.search(query, results=max_results)

            for title in search_results[:max_results]:
                try:
                    page = wikipedia.page(title)
                    results.append(
                        {
                            "title": page.title,
                            "url": page.url,
                            "snippet": (
                                page.summary[:300] + "..."
                                if len(page.summary) > 300
                                else page.summary
                            ),
                            "source": "Wikipedia",
                        }
                    )
                except wikipedia.exceptions.DisambiguationError as e:
                    # Try the first disambiguation option
                    try:
                        page = wikipedia.page(e.options[0])
                        results.append(
                            {
                                "title": page.title,
                                "url": page.url,
                                "snippet": (
                                    page.summary[:300] + "..."
                                    if len(page.summary) > 300
                                    else page.summary
                                ),
                                "source": "Wikipedia",
                            }
                        )
                    except:
                        continue
                except wikipedia.exceptions.PageError:
                    continue
                except Exception:
                    continue

            return results

        except Exception as e:
            raise Exception(f"Wikipedia search failed: {str(e)}")

    def search_github(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search GitHub repositories without authentication."""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": min(max_results, 100),
            }

            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            results = []

            for repo in data.get("items", [])[:max_results]:
                results.append(
                    {
                        "title": repo.get("full_name", ""),
                        "url": repo.get("html_url", ""),
                        "snippet": repo.get("description", "")
                        or "No description available",
                        "source": "GitHub",
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language", ""),
                        "updated": repo.get("updated_at", ""),
                    }
                )

            return results

        except Exception as e:
            raise Exception(f"GitHub search failed: {str(e)}")

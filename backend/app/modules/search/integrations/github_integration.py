from typing import List, Optional
import httpx
from app.modules.search.integrations.interfaces import IGitHubIntegration
from app.modules.search.schemas.response import GithubRepoItem
from app.core.config import settings


class GitHubIntegration(IGitHubIntegration):
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if settings.GITHUB_API_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_API_TOKEN}"

    async def search_repositories(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 10
    ) -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "page": page,
                "per_page": per_page,
                "sort": "stars",
                "order": "desc"
            }
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                "total_count": data.get("total_count", 0),
                "items": [
                    {
                        "id": item["id"],
                        "name": item["name"],
                        "full_name": item["full_name"],
                        "description": item.get("description"),
                        "html_url": item["html_url"],
                        "stargazers_count": item.get("stargazers_count", 0),
                        "language": item.get("language"),
                        "updated_at": item.get("updated_at", "")
                    }
                    for item in data.get("items", [])
                ]
            }

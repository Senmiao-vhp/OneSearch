from app.core.config import settings
from app.core.http_client import get_upstream_client


class GiteeIntegration:
    def __init__(self):
        self.base_url = "https://gitee.com/api/v5"
        self.headers = {
            "Accept": "application/json",
        }
        if settings.GITEE_API_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITEE_API_TOKEN}"

    async def search_repositories(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 10
    ) -> dict:
        client = get_upstream_client()
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": query,
            "page": page,
            "per_page": per_page,
            "sort": "stars_count",
            "order": "desc",
        }
        response = await client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "total": len(data) if isinstance(data, list) else 0,
            "items": [
                {
                    "id": item.get("id", 0),
                    "name": item.get("name", ""),
                    "full_name": item.get("full_name", ""),
                    "description": item.get("description"),
                    "html_url": item.get("html_url", ""),
                    "stargazers_count": item.get("stargazers_count", 0),
                    "language": item.get("language"),
                    "updated_at": item.get("updated_at", "")
                }
                for item in data if isinstance(data, list)
            ]
        }

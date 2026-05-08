from app.core.config import settings
from app.core.http_client import get_upstream_client
from app.modules.search.integrations.interfaces import IGiteeIntegration


class GiteeIntegration(IGiteeIntegration):
    """Gitee OpenAPI v5：GET /search/repositories，返回仓库数组（无总数字段）。"""

    def __init__(self):
        self.base_url = "https://gitee.com/api/v5"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "OneSearch/1.0",
        }

    async def search_repositories(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10,
    ) -> dict:
        client = get_upstream_client()
        params: dict = {
            "q": query,
            "page": page,
            "per_page": per_page,
            "sort": "stars_count",
            "order": "desc",
        }
        if settings.GITEE_ACCESS_TOKEN:
            params["access_token"] = settings.GITEE_ACCESS_TOKEN.strip()

        response = await client.get(
            f"{self.base_url}/search/repositories",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            msg = data.get("message") or str(data)
            raise ValueError(f"gitee 响应异常: {msg}")

        items_raw: list = data if isinstance(data, list) else []
        items = []
        for item in items_raw:
            full_name = (
                item.get("full_name")
                or item.get("path_with_namespace")
                or ""
            )
            items.append(
                {
                    "id": int(item.get("id") or 0),
                    "name": item.get("name") or "",
                    "full_name": full_name,
                    "description": item.get("description"),
                    "html_url": item.get("html_url") or "",
                    "stargazers_count": int(
                        item.get("stargazers_count")
                        or item.get("stars_count")
                        or 0
                    ),
                    "language": item.get("language"),
                    "updated_at": item.get("updated_at")
                    or item.get("last_push_at")
                    or "",
                }
            )

        return {"total_count": 0, "items": items}

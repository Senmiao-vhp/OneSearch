from app.core.http_client import get_upstream_client


class CsdnIntegration:
    def __init__(self):
        self.base_url = "https://so.csdn.net/api/v1/search"

    async def search_blogs(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 10
    ) -> dict:
        try:
            client = get_upstream_client()
            url = f"{self.base_url}/blog"
            params = {
                "q": query,
                "p": page,
                "size": per_page,
            }
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return {
                "total": data.get("data", {}).get("total", 0),
                "items": [
                    {
                        "id": item.get("id", ""),
                        "title": item.get("title", ""),
                        "description": item.get("description", ""),
                        "url": item.get("url", ""),
                        "author": item.get("author", ""),
                        "publish_time": item.get("created_at", ""),
                        "views": item.get("views", 0),
                    }
                    for item in data.get("data", {}).get("result", [])
                ]
            }
        except Exception as e:
            return {
                "total": 0,
                "items": [],
                "error": str(e)
            }

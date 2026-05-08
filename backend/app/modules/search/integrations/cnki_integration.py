from app.core.http_client import get_upstream_client


class CnkiIntegration:
    def __init__(self):
        self.base_url = "https://search.cnki.net"

    async def search_papers(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10
    ) -> dict:
        try:
            client = get_upstream_client()
            params = {
                "searchword": query,
                "PageIndex": page,
                "PageSize": per_page,
                "CategoryId": "",
                "IsLegal": "",
                "IsNovice": "",
                "SearchMType": "",
                "SearchType": "",
                "IsClub": "",
            }
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            return {
                "total": data.get("TotalCount", 0),
                "items": [
                    {
                        "id": item.get("ID", ""),
                        "title": item.get("Title", ""),
                        "authors": item.get("Authors", ""),
                        "journal": item.get("Source", ""),
                        "year": item.get("Year", ""),
                        "keywords": item.get("Keywords", ""),
                        "abstract": item.get("Abstract", ""),
                        "url": item.get("Url", ""),
                    }
                    for item in data.get("Data", [])
                ]
            }
        except Exception as e:
            return {
                "total": 0,
                "items": [],
                "error": str(e)
            }

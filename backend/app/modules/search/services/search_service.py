from app.modules.search.services.interfaces import ISearchService
from app.modules.search.integrations.interfaces import IGitHubIntegration


class SearchService(ISearchService):
    def __init__(self, github_integration: IGitHubIntegration):
        self.github_integration = github_integration

    async def search_github(self, query: str, page: int, per_page: int) -> dict:
        result = await self.github_integration.search_repositories(
            query=query,
            page=page,
            per_page=per_page
        )
        return {
            "total_count": result["total_count"],
            "page": page,
            "per_page": per_page,
            "items": result["items"]
        }

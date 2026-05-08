from fastapi import APIRouter, Depends, Query
from app.modules.search.schemas.response import GithubSearchResponse
from app.modules.search.services.search_service import SearchService
from app.modules.search.integrations.github_integration import GitHubIntegration


router = APIRouter(prefix="/search", tags=["搜索"])


def get_search_service() -> SearchService:
    return SearchService(GitHubIntegration())


@router.get("/github", response_model=GithubSearchResponse)
async def search_github(
    q: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量"),
    service: SearchService = Depends(get_search_service),
):
    result = await service.search_github(
        query=q,
        page=page,
        per_page=per_page
    )
    return result

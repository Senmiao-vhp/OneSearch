from fastapi import APIRouter, Depends, Query, HTTPException
from app.modules.search.schemas.response import GithubSearchResponse, MergedRepoSearchResponse
from app.modules.search.services.search_service import SearchService
from app.modules.search.integrations.github_integration import GitHubIntegration
from app.modules.search.integrations.gitee_integration import GiteeIntegration


router = APIRouter(prefix="/search", tags=["搜索"])


def get_search_service() -> SearchService:
    return SearchService(GitHubIntegration(), GiteeIntegration())


@router.get("/repos", response_model=MergedRepoSearchResponse)
async def search_repos_merged(
    q: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量"),
    service: SearchService = Depends(get_search_service),
):
    try:
        return await service.search_repos_merged(query=q, page=page, per_page=per_page)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


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

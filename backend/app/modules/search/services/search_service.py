from app.modules.search.services.interfaces import ISearchService
from app.modules.search.integrations.interfaces import IGitHubIntegration, IGiteeIntegration
import asyncio


class SearchService(ISearchService):
    def __init__(
        self,
        github_integration: IGitHubIntegration,
        gitee_integration: IGiteeIntegration,
    ):
        self.github_integration = github_integration
        self.gitee_integration = gitee_integration

    async def search_github(self, query: str, page: int, per_page: int) -> dict:
        result = await self.github_integration.search_repositories(
            query=query,
            page=page,
            per_page=per_page,
        )
        return {
            "total_count": result["total_count"],
            "page": page,
            "per_page": per_page,
            "items": result["items"],
        }

    async def search_repos_merged(self, query: str, page: int, per_page: int) -> dict:
        # 两源各拉满 per_page 条再合并打分；避免「一半给 Gitee」时 Gitee 为空导致本页只有一半条数
        gh_task = self.github_integration.search_repositories(
            query=query, page=page, per_page=per_page
        )
        gt_task = self.gitee_integration.search_repositories(
            query=query, page=page, per_page=per_page
        )

        gh_res, gt_res = await asyncio.gather(gh_task, gt_task, return_exceptions=True)

        items: list = []
        github_total = 0
        github_err: str | None = None
        gitee_err: str | None = None

        if isinstance(gh_res, Exception):
            github_err = str(gh_res)
        else:
            github_total = int(gh_res.get("total_count") or 0)
            for it in gh_res.get("items", []):
                items.append({**it, "source": "github"})

        if isinstance(gt_res, Exception):
            gitee_err = str(gt_res)
        else:
            for it in gt_res.get("items", []):
                items.append({**it, "source": "gitee"})

        if not items:
            if github_err and gitee_err:
                raise RuntimeError(
                    f"GitHub: {github_err}; Gitee: {gitee_err}"
                )

        items.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
        items = items[:per_page]

        return {
            "page": page,
            "per_page": per_page,
            "github_total_count": github_total,
            "items": items,
            "github_error": github_err,
            "gitee_error": gitee_err,
        }

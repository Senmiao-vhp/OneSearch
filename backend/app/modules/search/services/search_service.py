from app.modules.search.services.interfaces import ISearchService
from app.modules.search.integrations.interfaces import IGitHubIntegration, IGiteeIntegration
import asyncio


def _merge_github_gitee_fair(gh_items: list, gt_items: list, per_page: int) -> list:
    """两源各自按 Star 取配额后交错；避免全局排序时 GitHub 星标碾压导致页面无 Gitee。"""
    gh = sorted(
        gh_items,
        key=lambda x: x.get("stargazers_count", 0),
        reverse=True,
    )
    gt = sorted(
        gt_items,
        key=lambda x: x.get("stargazers_count", 0),
        reverse=True,
    )
    n_gh = (per_page + 1) // 2
    n_gt = per_page - n_gh

    gh_slice = [{**x, "source": "github"} for x in gh[:n_gh]]
    gt_slice = [{**x, "source": "gitee"} for x in gt[:n_gt]]

    out: list = []
    i = j = 0
    while len(out) < per_page:
        progressed = False
        if i < len(gh_slice):
            out.append(gh_slice[i])
            i += 1
            progressed = True
        if len(out) >= per_page:
            break
        if j < len(gt_slice):
            out.append(gt_slice[j])
            j += 1
            progressed = True
        if not progressed:
            break

    idx_gh = n_gh
    idx_gt = n_gt
    while len(out) < per_page and (idx_gh < len(gh) or idx_gt < len(gt)):
        if idx_gh < len(gh):
            out.append({**gh[idx_gh], "source": "github"})
            idx_gh += 1
        if len(out) >= per_page:
            break
        if idx_gt < len(gt):
            out.append({**gt[idx_gt], "source": "gitee"})
            idx_gt += 1

    return out[:per_page]


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
        # 两源各请求 per_page 条；合并时按源内 Star 取半屏配额并交错，避免全局排序全是 GitHub
        gh_task = self.github_integration.search_repositories(
            query=query, page=page, per_page=per_page
        )
        gt_task = self.gitee_integration.search_repositories(
            query=query, page=page, per_page=per_page
        )

        gh_res, gt_res = await asyncio.gather(gh_task, gt_task, return_exceptions=True)

        github_total = 0
        github_err: str | None = None
        gitee_err: str | None = None
        gh_raw: list = []
        gt_raw: list = []

        if isinstance(gh_res, Exception):
            github_err = str(gh_res)
        else:
            github_total = int(gh_res.get("total_count") or 0)
            gh_raw = gh_res.get("items") or []

        if isinstance(gt_res, Exception):
            gitee_err = str(gt_res)
        else:
            gt_raw = gt_res.get("items") or []

        if not gh_raw and not gt_raw:
            if github_err and gitee_err:
                raise RuntimeError(
                    f"GitHub: {github_err}; Gitee: {gitee_err}"
                )

        items = _merge_github_gitee_fair(gh_raw, gt_raw, per_page)

        return {
            "page": page,
            "per_page": per_page,
            "github_total_count": github_total,
            "items": items,
            "github_error": github_err,
            "gitee_error": gitee_err,
        }

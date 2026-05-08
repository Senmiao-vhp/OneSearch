"""合并搜索接口：依赖注入覆盖，不访问外网。"""
from fastapi.testclient import TestClient

from app.main import app
from app.modules.search.api import endpoints as search_endpoints


def test_search_repos_merged_orders_and_shape():
    """合并后按 Star 降序；响应含 source 字段。"""

    class _FakeSvc:
        async def search_github(self, *a, **kw):
            raise NotImplementedError

        async def search_repos_merged(self, query, page, per_page):
            return {
                "page": page,
                "per_page": per_page,
                "github_total_count": 100,
                "items": [
                    {
                        "id": 2,
                        "name": "high",
                        "full_name": "o/high",
                        "description": None,
                        "html_url": "https://example.com/2",
                        "stargazers_count": 99,
                        "language": "Rust",
                        "updated_at": "2026-01-01",
                        "source": "github",
                    },
                    {
                        "id": 1,
                        "name": "low",
                        "full_name": "o/low",
                        "description": None,
                        "html_url": "https://example.com/1",
                        "stargazers_count": 1,
                        "language": None,
                        "updated_at": "",
                        "source": "gitee",
                    },
                ],
                "github_error": None,
                "gitee_error": None,
            }

    app.dependency_overrides[search_endpoints.get_search_service] = lambda: _FakeSvc()
    try:
        c = TestClient(app)
        r = c.get(
            "/api/v1/search/repos",
            params={"q": "x", "page": 1, "per_page": 10},
        )
        assert r.status_code == 200
        data = r.json()
        assert data["items"][0]["stargazers_count"] == 99
        assert data["items"][0]["source"] == "github"
        assert data["items"][1]["source"] == "gitee"
    finally:
        app.dependency_overrides.clear()

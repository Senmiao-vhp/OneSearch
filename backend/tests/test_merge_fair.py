"""公平合并：高星全在 GitHub 时仍应插入 Gitee 条目。"""
from app.modules.search.services.search_service import _merge_github_gitee_fair


def test_fair_merge_interleaves_when_github_dominates_stars():
    gh = [
        {"id": 1, "stargazers_count": 1_000_000, "name": "gh1"},
        {"id": 2, "stargazers_count": 900_000, "name": "gh2"},
        {"id": 3, "stargazers_count": 800_000, "name": "gh3"},
        {"id": 4, "stargazers_count": 700_000, "name": "gh4"},
        {"id": 5, "stargazers_count": 600_000, "name": "gh5"},
        {"id": 6, "stargazers_count": 500_000, "name": "gh6"},
    ]
    gt = [
        {"id": 101, "stargazers_count": 500, "name": "gt1"},
        {"id": 102, "stargazers_count": 400, "name": "gt2"},
        {"id": 103, "stargazers_count": 300, "name": "gt3"},
        {"id": 104, "stargazers_count": 200, "name": "gt4"},
        {"id": 105, "stargazers_count": 100, "name": "gt5"},
    ]
    out = _merge_github_gitee_fair(gh, gt, per_page=10)
    assert len(out) == 10
    sources = [x["source"] for x in out]
    assert sources.count("gitee") >= 4  # 10 条里约一半为 Gitee 配额
    assert "gitee" in sources[:4]  # 交错前置区域含 Gitee


def test_fair_merge_one_side_empty():
    gh = [{"id": i, "stargazers_count": 100 - i} for i in range(10)]
    out = _merge_github_gitee_fair(gh, [], per_page=5)
    assert len(out) == 5
    assert all(x["source"] == "github" for x in out)
    assert len(_merge_github_gitee_fair([], [], 3)) == 0

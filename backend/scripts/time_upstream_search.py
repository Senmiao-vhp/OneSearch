"""本地耗时探测：GitHub / Gitee 搜索各请求一轮；不打印任何 Token。"""
from __future__ import annotations

import sys
from pathlib import Path

# 支持 `python scripts/time_upstream_search.py` 时的包路径
_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

import asyncio
import os
import time

import httpx

from app.core.http_client import close_upstream_client, get_upstream_client


def load_dotenv() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


async def main() -> None:
    load_dotenv()
    q = "python"
    per_page = 10

    gh_headers = {"Accept": "application/vnd.github+json"}
    t_gh = os.environ.get("GITHUB_API_TOKEN", "").strip()
    if t_gh:
        gh_headers["Authorization"] = f"Bearer {t_gh}"

    # 1) GitHub 单次
    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=120.0) as client:
        r_gh = await client.get(
            "https://api.github.com/search/repositories",
            params={"q": q, "per_page": per_page},
            headers=gh_headers,
        )
    e_gh = time.perf_counter() - t0
    n_gh = 0
    if r_gh.status_code == 200:
        n_gh = len(r_gh.json().get("items", []))
    print(f"[GitHub solo] HTTP {r_gh.status_code}  time {e_gh:.2f}s  items {n_gh}")

    # 2) Gitee 单次
    params: dict = {
        "q": q,
        "page": 1,
        "per_page": per_page,
        "sort": "stars_count",
        "order": "desc",
    }
    t_gt = os.environ.get("GITEE_ACCESS_TOKEN", "").strip()
    if t_gt:
        params["access_token"] = t_gt

    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=120.0) as client:
        r_gt = await client.get(
            "https://gitee.com/api/v5/search/repositories",
            params=params,
            headers={"Accept": "application/json", "User-Agent": "OneSearch-bench/1.0"},
        )
    e_gt = time.perf_counter() - t0
    body = r_gt.json()
    if isinstance(body, list):
        n_gt = len(body)
    else:
        n_gt = -1
    print(f"[Gitee  solo] HTTP {r_gt.status_code}  time {e_gt:.2f}s  items {n_gt}")

    # 3) asyncio.gather 并行（与后端合并搜索一致）
    async def gh_req() -> None:
        async with httpx.AsyncClient(timeout=120.0) as c:
            await c.get(
                "https://api.github.com/search/repositories",
                params={"q": q, "per_page": per_page},
                headers=gh_headers,
            )

    async def gt_req() -> None:
        async with httpx.AsyncClient(timeout=120.0) as c:
            await c.get(
                "https://gitee.com/api/v5/search/repositories",
                params=params,
                headers={"Accept": "application/json", "User-Agent": "OneSearch-bench/1.0"},
            )

    t0 = time.perf_counter()
    await asyncio.gather(gh_req(), gt_req())
    e_par = time.perf_counter() - t0
    print(f"[parallel gather] wall {e_par:.2f}s (about max(github,gitee))")

    # 第二轮：复用进程内共享 AsyncClient（与线上集成一致）
    async def gh2():
        c = get_upstream_client()
        await c.get(
            "https://api.github.com/search/repositories",
            params={"q": "rust", "per_page": per_page},
            headers=gh_headers,
        )

    async def gt2():
        p2 = {
            "q": "rust",
            "page": 1,
            "per_page": per_page,
            "sort": "stars_count",
            "order": "desc",
        }
        if t_gt:
            p2["access_token"] = t_gt
        c = get_upstream_client()
        await c.get(
            "https://gitee.com/api/v5/search/repositories",
            params=p2,
            headers={"Accept": "application/json"},
        )

    t0 = time.perf_counter()
    await asyncio.gather(gh2(), gt2())
    e_keep = time.perf_counter() - t0
    print(f"[parallel + shared client] wall {e_keep:.2f}s")

    await close_upstream_client()


if __name__ == "__main__":
    asyncio.run(main())

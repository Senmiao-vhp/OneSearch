"""探测 Gitee 搜索为何返回空列表；不打印 token。"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_BACKEND))

import httpx


def load_env() -> None:
    p = _BACKEND / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main() -> None:
    load_env()
    tok = (os.environ.get("GITEE_ACCESS_TOKEN") or "").strip()
    tok_set = bool(tok)

    cases: list[tuple[str, dict]] = [
        ("no_token_vue", {"q": "vue", "page": 1, "per_page": 5}),
        ("camel_perPage", {"q": "vue", "page": 1, "perPage": 5}),
        ("sort_empty", {"q": "vue", "page": 1, "per_page": 5, "sort": "", "order": "desc"}),
    ]
    if tok_set:
        cases.append(
            (
                "with_token_vue",
                {
                    "q": "vue",
                    "page": 1,
                    "per_page": 5,
                    "access_token": tok,
                },
            )
        )
        cases.append(
            (
                "with_token_python_sort",
                {
                    "q": "python",
                    "page": 1,
                    "per_page": 10,
                    "access_token": tok,
                    "sort": "stars_count",
                    "order": "desc",
                },
            )
        )

    h = {"Accept": "application/json", "User-Agent": "OneSearch-probe/1"}

    for name, params in cases:
        r = httpx.get(
            "https://gitee.com/api/v5/search/repositories",
            params=params,
            headers=h,
            timeout=60.0,
        )
        ct = r.headers.get("content-type", "")
        snippet = r.text[:200].replace("\n", " ")
        try:
            data = r.json()
        except Exception:
            print(f"{name}: HTTP {r.status_code} non-json body head={snippet!r}")
            continue
        if isinstance(data, list):
            print(f"{name}: HTTP {r.status_code} list_len={len(data)} head_item_keys={list(data[0].keys())[:6] if data else []}")
        else:
            print(f"{name}: HTTP {r.status_code} dict_keys={list(data.keys()) if isinstance(data, dict) else type(data)} body_snip={snippet!r}")

    print(f"GITEE_ACCESS_TOKEN set: {tok_set}")


if __name__ == "__main__":
    main()

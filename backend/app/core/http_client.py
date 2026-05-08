"""上游 HTTP 长连接复用，减少每次搜索新建 TLS。"""
from __future__ import annotations

import httpx

_client: httpx.AsyncClient | None = None

# 连接阶段单独限制，避免坏网络卡住过久；整体仍允许慢速读满
_TIMEOUT = httpx.Timeout(60.0, connect=15.0, read=60.0, write=30.0, pool=10.0)
_LIMITS = httpx.Limits(max_keepalive_connections=20, max_connections=40)


def get_upstream_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            timeout=_TIMEOUT,
            limits=_LIMITS,
            headers={"User-Agent": "OneSearch/1.0"},
        )
    return _client


async def close_upstream_client() -> None:
    global _client
    if _client is not None and not _client.is_closed:
        await _client.aclose()
    _client = None

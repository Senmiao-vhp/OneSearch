from pydantic import BaseModel
from typing import List, Literal, Optional


class GithubRepoItem(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    stargazers_count: int
    language: Optional[str] = None
    updated_at: str

    class Config:
        from_attributes = True


class GithubSearchResponse(BaseModel):
    total_count: int
    page: int
    per_page: int
    items: List[GithubRepoItem]


class GiteeRepoItem(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    stargazers_count: int
    language: Optional[str] = None
    updated_at: str

    class Config:
        from_attributes = True


class GiteeSearchResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[GiteeRepoItem]


class CsdnBlogItem(BaseModel):
    id: str
    title: str
    description: str
    url: str
    author: str
    publish_time: str
    views: int

    class Config:
        from_attributes = True


class CsdnSearchResponse(BaseModel):
    total: int
    items: List[CsdnBlogItem]


class CnkiPaperItem(BaseModel):
    id: str
    title: str
    authors: str
    journal: str
    year: str
    keywords: str
    abstract: str
    url: str

    class Config:
        from_attributes = True


class CnkiSearchResponse(BaseModel):
    total: int
    items: List[CnkiPaperItem]


class UnifiedRepoItem(GithubRepoItem):
    """合并 GitHub / Gitee 后的统一项。"""
    source: Literal["github", "gitee"]


class MergedRepoSearchResponse(BaseModel):
    page: int
    per_page: int
    github_total_count: int
    items: List[UnifiedRepoItem]
    github_error: Optional[str] = None
    gitee_error: Optional[str] = None

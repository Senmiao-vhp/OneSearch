from pydantic import BaseModel
from typing import List, Optional


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

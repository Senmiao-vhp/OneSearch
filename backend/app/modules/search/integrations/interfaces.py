from abc import ABC, abstractmethod
from typing import List


class IGitHubIntegration(ABC):
    @abstractmethod
    async def search_repositories(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 10
    ) -> dict:
        pass

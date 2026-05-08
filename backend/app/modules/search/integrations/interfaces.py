from abc import ABC, abstractmethod


class IGitHubIntegration(ABC):
    @abstractmethod
    async def search_repositories(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 10
    ) -> dict:
        pass


class IGiteeIntegration(ABC):
    @abstractmethod
    async def search_repositories(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10,
    ) -> dict:
        pass

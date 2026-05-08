from abc import ABC, abstractmethod


class ISearchService(ABC):
    @abstractmethod
    async def search_github(self, query: str, page: int, per_page: int) -> dict:
        pass

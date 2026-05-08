from abc import ABC, abstractmethod
from typing import Optional


class IAuthService(ABC):
    @abstractmethod
    async def register(self, email: str, username: str, password: str) -> dict:
        pass

    @abstractmethod
    async def login(self, login: str, password: str) -> dict:
        pass

    @abstractmethod
    async def get_current_user(self, user_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    async def logout(self) -> dict:
        pass

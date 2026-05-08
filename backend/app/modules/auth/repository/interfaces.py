from abc import ABC, abstractmethod
from typing import Optional
from app.modules.auth.schemas.request import RegisterRequest


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: RegisterRequest, password_hash: str) -> dict:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_email_or_username(self, login: str) -> Optional[dict]:
        pass

from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.schemas.request import RegisterRequest
from app.modules.auth.repository.interfaces import IUserRepository
from app.shared.models.users import User


class UserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: RegisterRequest, password_hash: str) -> dict:
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=password_hash
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
            "created_at": new_user.created_at.isoformat() if new_user.created_at else None
        }

    async def get_by_email(self, email: str) -> Optional[dict]:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "password_hash": user.password_hash,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        return None

    async def get_by_username(self, username: str) -> Optional[dict]:
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "password_hash": user.password_hash,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        return None

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        return None

    async def get_by_email_or_username(self, login: str) -> Optional[dict]:
        result = await self.db.execute(
            select(User).where(or_(User.email == login, User.username == login))
        )
        user = result.scalar_one_or_none()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "password_hash": user.password_hash,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        return None

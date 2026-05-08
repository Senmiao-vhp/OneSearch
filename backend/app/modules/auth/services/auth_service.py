from typing import Optional
from app.modules.auth.services.interfaces import IAuthService
from app.modules.auth.repository.interfaces import IUserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException, NotFoundException
from app.modules.auth.schemas.request import RegisterRequest


class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, username: str, password: str) -> dict:
        existing_email = await self.user_repository.get_by_email(email)
        if existing_email:
            raise UserAlreadyExistsException("该邮箱已被注册")

        existing_username = await self.user_repository.get_by_username(username)
        if existing_username:
            raise UserAlreadyExistsException("该用户名已被使用")

        password_hash = get_password_hash(password)
        
        request_data = RegisterRequest(email=email, username=username, password=password)
        user = await self.user_repository.create(request_data, password_hash)
        
        return user

    async def login(self, login: str, password: str) -> dict:
        user = await self.user_repository.get_by_email_or_username(login)
        if not user:
            raise InvalidCredentialsException()

        if not verify_password(password, user["password_hash"]):
            raise InvalidCredentialsException()

        token = create_access_token(data={"sub": str(user["id"])})
        
        return {
            "id": user["id"],
            "email": user["email"],
            "username": user["username"],
            "token": token
        }

    async def get_current_user(self, user_id: int) -> Optional[dict]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("用户不存在")
        return user

    async def logout(self) -> dict:
        return {"message": "登出成功"}

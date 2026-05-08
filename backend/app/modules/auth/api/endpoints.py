from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.modules.auth.schemas.request import RegisterRequest, LoginRequest
from app.modules.auth.schemas.response import UserResponse, MessageResponse
from app.modules.auth.services.auth_service import AuthService
from app.modules.auth.repository.user_repository import UserRepository
from app.core.database import get_db
from app.shared.dependencies import get_current_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token


router = APIRouter(prefix="/auth", tags=["认证"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    request: RegisterRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.register(
        email=request.email,
        username=request.username,
        password=request.password
    )
    return user


@router.post("/login", response_model=UserResponse)
async def login(
    request: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.login(
        login=request.login,
        password=request.password
    )
    
    token = create_access_token(data={"sub": str(result["id"])})
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        max_age=604800,
        samesite="lax",
        secure=False
    )
    
    return {
        "id": result["id"],
        "email": result["email"],
        "username": result["username"]
    }


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response):
    response.delete_cookie(key="token", path="/")
    return {"message": "登出成功"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
):
    user = await service.get_current_user(user_id)
    return user

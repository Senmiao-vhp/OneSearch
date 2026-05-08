from fastapi import Depends, Cookie
from typing import Optional
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException


async def get_current_user_id(token: Optional[str] = Cookie(None)) -> int:
    if not token:
        raise UnauthorizedException("未登录")
    
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Token无效")
    
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token无效")
    
    return int(user_id)


def get_optional_user_id(token: Optional[str] = Cookie(None)) -> Optional[int]:
    if not token:
        return None
    
    payload = decode_access_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    return int(user_id)

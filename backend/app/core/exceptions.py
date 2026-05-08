from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, code: int, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        super().__init__(status_code=status_code, detail=message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "认证失败"):
        super().__init__(code=1002, message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    def __init__(self, message: str = "权限不足"):
        super().__init__(code=1003, message=message, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundException(AppException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=404, message=message, status_code=status.HTTP_404_NOT_FOUND)


class UserAlreadyExistsException(AppException):
    def __init__(self, message: str = "用户已存在"):
        super().__init__(code=2001, message=message, status_code=status.HTTP_409_CONFLICT)


class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "用户名或密码错误"):
        super().__init__(code=2003, message=message, status_code=status.HTTP_401_UNAUTHORIZED)

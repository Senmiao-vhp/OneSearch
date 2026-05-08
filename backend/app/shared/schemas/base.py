from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class ResponseBase(BaseModel):
    code: int = 0
    message: str = "success"


class DataResponse(ResponseBase, Generic[T]):
    data: Optional[T] = None


class ListResponse(ResponseBase, Generic[T]):
    data: Optional[T] = None
    total: int = 0
    page: int = 1
    per_page: int = 10

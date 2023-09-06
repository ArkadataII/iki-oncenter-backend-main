from datetime import datetime
from typing import Optional, TypeVar, Generic, Union, Any, List
from pydantic.generics import GenericModel
from pydantic import BaseModel
from fastapi import status

T = TypeVar("T")


class BaseResponseSerialization(BaseModel):
    id: int
    is_active: bool
    created_at: datetime = None
    updated_at: datetime = None


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: Union[str, Any], message: str):
        self.code = status.HTTP_200_OK
        self.message = message
        return self

    def success_response(self):
        self.code = status.HTTP_200_OK
        self.message = 'Thành công'
        return self


class DataResponse(GenericModel, Generic[T]):
    code: Union[int, str] = status.HTTP_200_OK
    message: Optional[str] = "Thành công"
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def success_response(self, data: T, code: Union[int, str] = code, message: Optional[Any] = message):
        self.code = code
        self.message = message
        self.data = data

        return self


class DataResponseGateway(GenericModel, Generic[T]):
    statusCode: int = None
    status: bool = None
    error: List[str] = []
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def success(cls, statusCode: int, status=True, data: Any = None):
        return cls(statusCode=statusCode, status=status, data=data)

    @classmethod
    def errors(cls, statusCode: int, status=False, error: List[str] = []):
        return cls(statusCode=statusCode, status=status, error=error)


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int

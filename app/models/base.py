from datetime import datetime
from pydantic import validator

from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr

DeclarativeBase = declarative_base()


@as_declarative()
class BaseCustom:
    __abstract__ = True
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(BaseCustom):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column('is_active', Boolean, index=True, default=True)
    created_at = Column('created_at', DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column('updated_at', DateTime(timezone=True), default=func.now(), onupdate=func.now())

    class Config:
        orm_mode = True

    @validator("created_at", "updated_at", pre=True)
    async def default_datetime(
            cls,  # noqa: N805
            value: datetime,  # noqa: WPS110
    ) -> datetime:
        return value or datetime.now()

    async def json(self, **kwargs):
        include = getattr(self.Config, "include", set())
        if len(include) == 0:
            include = None
        exclude = getattr(self.Config, "exclude", set())
        if len(exclude) == 0:
            exclude = None
        return super().json(include=include, exclude=exclude, **kwargs)

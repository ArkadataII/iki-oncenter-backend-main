from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.helpers.paging import PaginationParams, paginate
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    _instances = {}

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(CRUDBase, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]

    def get(self, db: Session, id: Any) -> Optional[ModelType]:

        return db.query(self.model).filter(self.model.id == id, self.model.is_active == True).first()

    def list(self, db: Session, *, query: Query, params: Optional[PaginationParams]) -> Optional[Any]:
        results = paginate(model=self.model, query=query, params=params)

        return results

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)

        db.delete(obj)
        db.commit()

        return obj

    def destroy(self, db: Session, *, db_obj: ModelType) -> ModelType:
        db_obj.is_active = False

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

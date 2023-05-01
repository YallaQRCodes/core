"""
## Description
CRUD abstraction base class.
## Usage
```python3
from yqrc_core.crud_base import CRUDBase
from my_models import MyModel
from my_schemas import MyCreateSchema, MyUpdateSchema

class MyCRUD(CRUDBase[MyModel, MyCreateSchema, MyUpdateSchema]):
    ...

my_crud: MyCRUD = MyCRUD(MyModel)
my_obj: MyModel = my_crud.get(db=db_session, id=my_object_id)
```
"""
from typing import (Any, Dict, Generic, List, Optional, Sequence, Type,
                    TypeVar, Union)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .models_base import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Implements all basic crud functionality.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Returns the sqlalchemy object with passed id.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Returns a list of #limit sqlalchemy objects from skip.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Creates and returns sqlalchemy object with the passed pydantic schema.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi(
        self, db: Session, *, objs_in: List[CreateSchemaType]
    ) -> Sequence[ModelType]:
        """
        Creates and returns multiple sqlalchemy objects with the passed
        pydantic schemas.
        """
        db_objs = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            db_objs.append(db_obj)
        return db_objs

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Updates and returns sqlalchemy object with the passed pydantic schema.
        """
        # XXX(gaytomycode): This should update a copy of the db_obj not the
        # db_obj itself to allow the user to keep a copy of the old db_objs
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

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        Removes and returns the object with the passed id
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

"""
## Description
Sqlachemy model base class.
## Usage
```python3
from yqrc_core.models_base import Base

class MyModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    ...

```
"""
from typing import Any, Dict

from sqlalchemy.ext.declarative import as_declarative, declared_attr

__class_registry: Dict = {}


@as_declarative(class_registry=__class_registry)
class Base:
    """
    The base for the sqlalchemy models. Sets the tablename to lower case class
    name.
    """

    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

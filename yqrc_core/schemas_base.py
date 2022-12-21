"""
## Description
Pydantic base class with decorated property methods supported.
## Usage
```python3
from yqrc_core.schemas_base import PropertyBaseModel

class MySchema(PropertyBaseModel):
    example: str

    @property
    def example(self):
        return 'example'

```
"""
from pydantic import BaseModel
from typing import Union


class PropertyBaseModel(BaseModel):
    """
    Allows adding on the fly calculations with property decorator.
    """

    @classmethod
    def get_properties(cls):
        return [
            prop
            for prop in dir(cls)
            if isinstance(getattr(cls, prop), property)
            and prop not in ('__values__', 'fields')
        ]

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'DictStrAny':
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        props = self.get_properties()
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})

        return attribs

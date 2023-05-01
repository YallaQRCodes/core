"""
## Description
Pydantic settings instance
## Usage
```python3
from yqrc_core.config import settings

settings.MEDIA_ROOT
```
"""
import json
import os
import re
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, Field, validator


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)


class Settings(BaseSettings):
    """
    The settings used by micro-services
    """

    MEDIA_ROOT: str = os.path.join(os.getcwd(), 'media')
    """Path to file upload. Now is local but should be moved to AWS S3"""

    SQLALCHEMY_DATABASE_URI: str = 'postgresql+psycopg2://user:pass@host:p/db'
    """Path to the database. Now is local but should be moved to AWS RDS"""

    JWT_SECRET: str = ''
    """Used by the identity micro-service to create JWTs"""
    ALGORITHM: str = 'HS256'
    """Used by the identity micro-service to create JWTs"""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    """Used by the identity micro-service to create JWTs"""

    API_V1_STR: str = '/v1'
    """Route prefix for version 1"""

    BACKEND_CORS_ORIGINS: List = []
    """Allowed cors origins. Can take str, list, regex"""

    BACKEND_URI: AnyHttpUrl = Field('http://localhost:8000')
    """Micro-service URI"""
    FRONTEND_URI: AnyHttpUrl = Field('http://localhost:3000')
    """FrontEnd URI"""

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def __assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        """
        Validates and formats CORS origins
        """
        if isinstance(v, str) and not v.startswith('['):
            return [re.compile(i.strip()) for i in v.split(',')]
        elif isinstance(v, (list, str)):
            print('HELLO')
            print([i for i in v])
            print([re.compile(i) for i in v])
            return [re.compile(i) for i in v]
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = '.env'
        json_loads = LazyDecoder().decode
        """
        Now is a local file but should be moved to AWS lambda env
        """


settings = Settings()
"""The settings instance that is used by the micro-services"""

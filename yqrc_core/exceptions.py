"""
## Description
HTTP Exceptions.
## Usage
```python3
from yqrc_core.exceptions import app_exceptions

for exc in app_exceptions:
    app.add_exception_handler(exc['err'], exc['defn'])

```
"""
from fastapi import Request
from fastapi.responses import JSONResponse

app_exceptions = []


def __export(err):
    def _(defn):
        app_exceptions.append({'err': err, 'defn': defn})

    return _


class Unauthorized(Exception):
    """An exception raised when user is not authorized."""


class InvalidRequest(Exception):
    """An exception raised when a request is not valid"""


class RateLimited(Exception):
    """An exception raised when you hit a rate limit"""

    def __init__(self, json, headers):
        self.json = json
        self.headers = headers
        self.message = json['message']
        self.retry_after = json['retry_after']
        super().__init__(self.message)


class InvalidToken(Exception):
    """An exception raised when a response has invalid tokens"""


class ScopeMissing(Exception):
    scope: str

    def __init__(self, scope: str):
        self.scope = scope
        super().__init__(self.scope)


@__export(Unauthorized)
def unauthorized_exception_handler(request: Request, exc: Unauthorized):
    return JSONResponse({'error': 'Unauthorized'}, status_code=401)


@__export(RateLimited)
def rate_limit_exception_handler(request: Request, exc: RateLimited):
    return JSONResponse(
        {
            'error': 'RateLimited',
            'retry': exc.retry_after,
            'message': exc.message,
        },
        status_code=429,
    )

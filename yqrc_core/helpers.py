"""
## Description
Couple of helper functions.
"""
from typing import Optional, Dict, Any
import http.client
import json
import re


def ord(n: int) -> str:
    """
    Prefix numbers with their order.

    >>> from yqrc_core.helpers import ord
    >>> ord(13)
    '13th'
    >>> ord(22)
    '22nd'
    """
    return str(n) + (
        'th'
        if 4 <= n % 100 <= 20
        else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    )


def validate_url(url: str) -> Optional[re.Match]:
    """
    Take a url and checks if it is valid

    - starts with http or https
    - contains at least one "." between the TLD and the domain name
    - the domain name is composed of letters, numbers _ and -
    - the URL is delimited at the end by a space and can contain any other
        character

    >>> from yqrc_core.helpers import validate_url
    >>> validate_url('https://www.youtube.com')
    True
    >>> validate_url('youtube')
    False
    """
    url_regex = '^https?://[\\w\\-]+(\\.[\\w\\-]+)+\\S*'
    return re.match(url_regex, url)


def fix_url(valid_url: str) -> str:
    """
    Take a url and adds http if http or https are missing.

    >>> from yqrc_core.helpers import fix_url
    >>> validate_url('www.youtube.com')
    'http://www.youtube.com'
    """
    return 'http://' + valid_url.strip()


# XXX(gaytomycode): A request handler that works, should improve it thou to our
# needs
GET: str = 'GET'
POST: str = 'POST'

STATUS_CODE: Dict[int, str] = {}


class Request:
    def __init__(
        self,
        url: str,
        path: str,
        method: str = GET,
        headers: dict[str, str] = {},
        json: dict[str, Any] = {},
    ):
        self.__url = url
        self.__path = path
        self.__method = method
        self.__headers = {
            **headers,
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        self.__req_json = json

    def send(self):
        conn = http.client.HTTPSConnection(self.__url)
        conn.request(
            self.__method,
            self.__path,
            json.dumps(self.__req_json),
            headers=self.__headers,
        )
        resp = conn.getresponse()
        if resp.status // 100 != 2:
            # XXX(gaytomycode): raising an error here is stupid ik this is a
            # tmp class (azon?)
            raise ValueError(f'{resp.status} {resp.reason} {resp.read()}')
        return {
            'status': resp.status,
            'json': json.loads(resp.read()),
        }

    def set_auth_header(self, value):
        self.__headers['Authorization'] = value

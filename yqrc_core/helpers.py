"""
## Description
Couple of helper functions.
"""
import re
from typing import Optional


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

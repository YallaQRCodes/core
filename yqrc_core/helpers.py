"""
## Description
Couple of helper functions.
"""


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

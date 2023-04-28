"""
    Url TypedDict model from CC API responses.
"""
from typing import TypedDict, Optional


class UrlLink(TypedDict):
    """
    Single url link.
    """
    href: str


class UrlLinks(TypedDict):
    """
    Url links in url field `_links`.
    """
    qr: UrlLink
    stats: Optional[UrlLink]


class Url(TypedDict):
    """
    Url model from API.
    """
    id: int
    redirect_url: str
    hash: str
    expires_at: float
    is_expired: bool
    stats_is_public: bool
    is_deleted: bool
    _links: UrlLinks


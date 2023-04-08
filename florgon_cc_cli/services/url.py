"""
    Services for working with single url API.
"""


from os import access
from typing import Any, Dict, Tuple, Optional

from florgon_cc_cli.services.api import execute_api_method
from florgon_cc_cli import config


def build_open_url(hash: str) -> str:
    """Builds url for opening short url."""
    return f"{config.URL_OPEN_PROVIDER}/{hash}"


def create_url(
    long_url: str, stats_is_public: bool = False, access_token: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Creates short url from long url.
    :param str long_url: url which short url will be redirect
    :param Optional[str] auth_token: Florgon OAuth token that used for authentification. Defaults to None
    :return: Tuple with two elements.
             First is a creaton status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[bool, Dict[str, Any]]
    """
    response = execute_api_method(
        "POST",
        "urls/",
        data={"url": long_url, "stats_is_public": stats_is_public},
        access_token=access_token,
    )

    if "success" in response:
        return True, response["success"]["url"]
    return False, response["error"]


def get_url_info_by_hash(hash: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Returns info about short url by hash.
    :param str hash: short url hash
    :return: Tuple with two elements.
             First is a creaton status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[bool, Dict[str, any]]
    """
    response = execute_api_method("GET", f"urls/{hash}/")
    if "success" in response:
        return True, response["success"]["url"]
    return False, response["error"]

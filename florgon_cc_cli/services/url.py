"""
    Services for working with single url API.
"""
import re
from typing import Any, Dict, Tuple, Optional

import click

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
             First is a response status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[bool, Dict[str, any]]
    """
    response = execute_api_method("GET", f"urls/{hash}/")
    if "success" in response:
        return True, response["success"]["url"]
    return False, response["error"]



def get_url_stats_by_hash(
    hash: str,
    url_views_by_referers_as: str = "percent",
    url_views_by_dates_as: str = "percent",
    access_token: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Returns statistics about short url by hash.
    :param str hash: short url hash
    :return: Tuple with two elements.
             First is a response status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[bool, Dict[str, any]]
    """
    response = execute_api_method("GET", f"urls/{hash}/stats", params={
        "referer_views_value_as": url_views_by_referers_as,
        "dates_views_value_as": url_views_by_dates_as,
    }, access_token=access_token)
    if "success" in response:
        return True, response["success"]["views"]
    return False, response["error"]


def extract_hash_from_short_url(short_url: str) -> str:
    """
    Extracts hash from short url.
    :param str short_url: short url
    :rtype: str
    :return: url hash
    """
    short_url_hashes = re.findall(f"^{config.URL_OPEN_PROVIDER}" + r"/([a-zA-Z0-9]{6})$", short_url)
    if not short_url_hashes:
        click.secho(
            f"Short url is invalid! It should be in form '{config.URL_OPEN_PROVIDER}/xxxxxx'",
            err=True,
            fg="red",
        )
        click.get_current_context().exit(1)

    return short_url_hashes[0]


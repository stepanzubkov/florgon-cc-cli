"""
    Services for working with Florgon CC Api.
"""
from typing import Any, Dict, Optional

import requests

import florgon_cc_cli.config as config
from florgon_cc_cli.services.config import get_value_from_config


def execute_api_method(
    http_method: str,
    api_method: str,
    *,
    data: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes API method.
    :param str http_method: GET, POST, PUT, PATCH, DELETE or OPTIONS
    :param str api_method: API method, described in docs
    :param Dict[str, Any] data: POST JSON data
    :param Dict[str, Any] params: GET data
    :param Optional[str] access_token: Florgon OAuth token
    :rtype: Dict[str, Any]
    :return: JSON response from API
    """
    request_url = f"{get_api_host()}/{api_method}"
    response = requests.request(
        http_method,
        request_url,
        json=data,
        params=params,
        headers={"Authorization": access_token} if access_token else {},
    )
    return response.json()


def get_api_host() -> str:
    """
    Returns API host from user config. If it is not set, returns default API host.
    :rtype: str
    :return: API host
    """
    return get_value_from_config("api_host") or config.CC_API_URL


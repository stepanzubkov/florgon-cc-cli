"""
    Services for working with Florgon CC Api.
"""
from typing import Any, Dict

import requests

import florgon_cc_cli.config as config


def execute_api_method(
    http_method: str,
    api_method: str,
    *,
    data: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    access_token: str | None = None,
) -> Dict[str, Any]:
    request_url = f"{config.CC_API_URL}/{api_method}"
    response = requests.request(
        http_method,
        request_url,
        json=data,
        params=params,
        headers={"Authorization": access_token} if access_token else {},
    )
    return response.json()

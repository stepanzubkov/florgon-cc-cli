"""
    Services for working with Florgon CC Api.
"""
from typing import Any, Dict, Optional, NoReturn, Union

import requests
import click

import florgon_cc_cli.config as config
from florgon_cc_cli.services.config import get_value_from_config


def execute_json_api_method(
    http_method: str,
    api_method: str,
    *,
    data: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    access_token: Optional[str] = None,
) -> Dict[str, Any] | NoReturn:
    """
    Executes API method.
    :param str http_method: GET, POST, PUT, PATCH, DELETE or OPTIONS
    :param str api_method: API method, described in docs
    :param Dict[str, Any] data: POST JSON data
    :param Dict[str, Any] params: GET data
    :param Optional[str] access_token: Florgon OAuth token
    :rtype: Union[Dict[str, Any], NoResponse]
    :return: JSON response from API or exit application
    """
    response = execute_api_method(
        http_method,
        api_method,
        data=data,
        params=params,
        access_token=access_token,
    )
    return try_decode_response_to_json(response)


def execute_api_method(
    http_method: str,
    api_method: str,
    *,
    data: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    access_token: Optional[str] = None,
) -> requests.Request:
    """
    Executes API method and returns Request object.
    :param str http_method: GET, POST, PUT, PATCH, DELETE or OPTIONS
    :param str api_method: API method, described in docs
    :param Dict[str, Any] data: POST JSON data
    :param Dict[str, Any] params: GET data
    :param Optional[str] access_token: Florgon OAuth token
    :rtype: requests.Response
    :return: response object
    """
    request_url = f"{get_api_host()}/{api_method}"
    response = requests.request(
        http_method,
        request_url,
        json=data,
        params=params,
        headers={"Authorization": access_token} if access_token else {},
    )
    ctx = click.get_current_context()
    if ctx.obj["DEBUG"]:
        click.secho(
            f"API response from {request_url} with HTTP code {response.status_code}:", fg="yellow"
        )
        click.echo(response.text)

    return response


def get_api_host() -> str:
    """
    Returns API host from user config. If it is not set, returns default API host.
    :rtype: str
    :return: API host
    """
    return get_value_from_config("api_host") or config.CC_API_URL


def try_decode_response_to_json(response: requests.Response) -> Union[Dict[str, Any], NoReturn]:
    """
    Tries to decode response to json.
    :param requests.Response response: response object
    :return: JSON dict if decoding is successfully, else exit application
    :rtype: Union[Dict[str, Any], NoReturn]
    """
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        ctx = click.get_current_context()
        click.secho("Unable to decode API response as JSON!", fg="red", err=True)
        ctx.exit(1)

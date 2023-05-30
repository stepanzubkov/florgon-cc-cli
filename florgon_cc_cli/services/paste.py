"""
    Services for working with single paste API or list.
"""
from typing import Optional, Tuple, Union, NoReturn

import click

from pick import pick
from florgon_cc_cli.models.url import Url
from florgon_cc_cli.services.api import execute_json_api_method, execute_api_method, try_decode_response_to_json
from florgon_cc_cli import config
from florgon_cc_cli.models.paste import Paste
from florgon_cc_cli.models.error import Error
from florgon_cc_cli.services.api import execute_json_api_method
from florgon_cc_cli.services.config import get_value_from_config


def build_paste_open_url(hash: str) -> str:
    """Builds url for opening paste."""
    return f"{config.URL_PASTE_OPEN_PROVIDER}/{hash}"


def create_paste(
    text: str,
    *,
    stats_is_public: bool = False,
    burn_after_read: bool = False,
    access_token: Optional[str] = None,
) -> Tuple[bool, Union[Paste, Error]]:
    """
    Creates paste from text.
    :param str text: paste text
    :param Optional[str] access_token: Florgon OAuth token that used for authorization.
                                     Defaults to None
    :param bool stats_is_public: makes url stats public for all users
    :param bool burn_after_read: paste will be deleted after first reading
    :return: Tuple with two elements.
             First is a creaton status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[True, Paste] if request is successfully, else Tuple[False, Error]
    """
    response = execute_json_api_method(
        "POST",
        "pastes/",
        data={"text": text, "stats_is_public": stats_is_public, "burn_after_read": burn_after_read},
        access_token=access_token,
    )
    if "success" in response:
        return True, response["success"]["paste"]
    return False, response["error"]


def get_pastes_list(access_token: Optional[str] = None) -> Tuple[bool, Union[Paste, Error]]:
    """
    Returns list of user pastes by access_token.
    :param Optional[str] access_token: Florgon OAuth token that used for authorization.
                                       Defaults to None.
    :rtype: Tuple[True, Paste] if successfully, else Tuple[False, Error]
    :return: Tuple with two elements.
             First is a response status (True if successfully).
             Seconds is a response body.
    """
    response = execute_json_api_method(
        "GET",
        "pastes/",
        access_token=access_token,
    )
    if "success" in response:
        return True, response["success"]["pastes"]
    return False, response["error"]

def build_open_url(hash: str) -> str:
    """Builds url for opening short url."""
    return f"{config.URL_PASTE_OPEN_PROVIDER}/{hash}"


def request_hash_from_urls_list() -> str:
    success, response = get_pastes_list(access_token=get_value_from_config("access_token"))
    if not success:
        click.secho(response["message"], err=True, fg="red")
        click.get_current_context().exit(1)

    # TODO: This logic must be moved to API
    response = [url for url in response if not url["is_expired"]]

    urls = [
        f"{build_open_url(url['hash'])} - {url['redirect_url']}"
        for url in response
    ]
    _, index = pick(urls, "Choose one from your urls:", indicator=">")
    return response[index]["hash"]

def get_url_info_by_hash(hash: str) -> Tuple[bool, Union[Url, Error]]:
    """
    Returns info about short url by hash.
    :param str hash: short url hash
    :return: Tuple with two elements.
             First is a response status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[True, Url] if request is successfully, else Tuple[True, Error]
    """
    response = execute_json_api_method("GET", f"pastes/{hash}/")
    if "success" in response:
        return True, response["success"]["paste"]
    return False, response["error"]

def delete_url_by_hash(hash: str, access_token: Optional[str] = None) -> Union[Tuple[bool, Optional[Error]], NoReturn]:
    """
    Deletes user's url by access_token.
    :param str hash: url hash
    :param Optional[str] access_token: access token
    :return: Tuple with two or one elements.
             First is a deletion status (True if successfully).
             Seconds is a response body (if error).
    :rtype: Tuple[True] if successfully deleted, Tuple[False, Error] if error occured,
            or exit application if cannot decode to json
    """
    response = execute_api_method("DELETE", f"pastes/{hash}/", access_token=access_token)
    if response.status_code == 204:
        return True,
    return try_decode_response_to_json(response)

"""
    Services for working with single paste API or list.
"""
from typing import Optional, Tuple, Union

from florgon_cc_cli.services.api import execute_json_api_method
from florgon_cc_cli import config
from florgon_cc_cli.models.paste import Paste
from florgon_cc_cli.models.error import Error
from florgon_cc_cli.services.api import execute_json_api_method


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

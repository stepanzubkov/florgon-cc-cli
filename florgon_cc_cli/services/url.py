"""
    Services for working with single url API.
"""


from typing import Any, Dict, Tuple

from florgon_cc_cli.services.api import execute_api_method
import florgon_cc_cli.config as config


def build_open_url(hash: str) -> str:
    return f"{config.URL_OPEN_PROVIDER}/{hash}"


def create_url(long_url: str, auth_token: str | None = None) -> Tuple[bool, Dict[str, Any]]:
    response = execute_api_method("POST", "urls/", data={"url": long_url})

    if "success" in response:
        return True, response["success"]["url"]
    else:
        return False, response["error"]

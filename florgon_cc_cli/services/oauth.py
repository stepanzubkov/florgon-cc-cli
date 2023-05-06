"""
    Services for interaction with Florgon OAuth.
"""
from typing import Optional
import re


def build_sso_login_url(
    client_id: int = 1,
    scope: str = "cc",
    response_type: str = "token",
    redirect_uri: str = "https://florgon.com/oauth/blank",
    oauth_screen_url: str = "https://florgon.com/oauth/authorize",
) -> str:
    """
    Returns url for OAuth user login manually.
    :param int client_id: ID of Florgon OAuth client. Defaults to 1,
    :param str scope: OAuth scope. Defaults to "cc"
    :param str response_type: Type of OAuth response. Defaults to"token"
    :param str redirect_uri: Url that user will redirected to.
    Defaults to "https://florgon.com/oauth/blank"
    :param str oauth_screen_url: Login page url. Defaults to "https://florgon.com/oauth/authorize"
    """
    return (
        f"{oauth_screen_url}?client_id={client_id}&redirect_uri={redirect_uri}"
        f"&scope={scope}&response_type={response_type}"
    )


def extract_token_from_redirect_uri(redirect_uri: str) -> Optional[str]:
    """
    Extracts access token from hash parameters from redirect_uri.
    :param str redirect_uri: redirect uri from oauth
    :rtype: Optional[str]
    :returns: token
    """
    tokens = re.findall(r"#token=([\w-]+\.[\w-]+\.[\w-]+)&", redirect_uri)
    if len(tokens) == 1:
        return tokens[0]

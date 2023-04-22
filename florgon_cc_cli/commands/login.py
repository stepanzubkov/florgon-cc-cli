"""
    Commands to login to Florgon.
"""
import click
from florgon_cc_cli.services.config import save_value_to_config

from florgon_cc_cli.services.oauth import build_sso_login_url, extract_token_from_redirect_uri


@click.command()
def login():
    """
    Login to Florgon.
    """
    redirect_uri = click.prompt(
        "Please, visit \n"
        + click.style(build_sso_login_url(), fg="green")
        + "\nthen login, and paste redirect url here"
    )
    token = extract_token_from_redirect_uri(redirect_uri)
    if token is None:
        click.secho("Url is invalid. Please relogin!", fg="red", err=True)
        return

    save_value_to_config("access_token", token)
    click.secho("You are logged in successfully!", fg="green")

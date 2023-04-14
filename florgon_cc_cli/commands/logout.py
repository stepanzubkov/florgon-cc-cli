"""
    Command for logging out.
"""
import click

from florgon_cc_cli.services.config import delete_value_from_config, get_value_from_config


@click.command()
def logout():
    """
    Deletes auth data.
    """
    if get_value_from_config("access_token") is None:
        click.secho("You are not logged in!", fg="red", err=True)
        return

    delete_value_from_config("access_token")
    click.secho("You are successfully logged out!", fg="green")

"""
    Sets API host.
"""
import click

from florgon_cc_cli.services.config import get_value_from_config, save_value_to_config
from florgon_cc_cli import config


@click.group()
def host():
    pass


@host.command()
@click.argument("host", type=str)
def set(host):
    """
    Sets API host.
    """
    save_value_to_config("api_host", host)
    click.echo("API host changed to " + click.style(host, fg="green"))


@host.command()
def get():
    """
    Prints current API host.
    """
    click.echo(get_value_from_config("api_host") or config.CC_API_URL)

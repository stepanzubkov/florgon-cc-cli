"""
    Command for working with user config
"""
import click

import florgon_cc_cli.config
from florgon_cc_cli.services.config import deserialize_config


@click.group()
def config():
    """
    Work with user config.
    """


@config.command()
@click.option(
    "-r", "--raw", is_flag=True, default=False, help="Prints config 'as is', in toml format."
)
def show(raw: bool):
    """
    Prints user config.
    """
    if raw:
        with open(florgon_cc_cli.config.CONFIG_FILE, "r") as f:
            click.echo(f.read())
        return

    user_config = deserialize_config()
    for key, value in user_config.items():
        click.echo(click.style(f"{key:20}", fg="green") + f"\t{value}")

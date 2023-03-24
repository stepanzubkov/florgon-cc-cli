"""
    Single url commands.
"""
from datetime import datetime

import click

from florgon_cc_cli.services.url import build_open_url, create_url


@click.group()
def url():
    """Commands that interacts with single url."""


@url.command()
@click.option("-o", "--only-url", is_flag=True, default=False, help="Outputs single short url.")
@click.option(
    "-d", "--do-not-save", is_flag=True, default=False, help="Do not save url in local history."
)
@click.argument("long_url", type=str)
def create(only_url: bool, do_not_save: bool, long_url: str):
    """Creates short url."""
    success, response = create_url(long_url)
    if not success:
        click.secho(response["message"], err=True, fg="red")
        return

    short_url = build_open_url(response["hash"])
    if only_url:
        click.echo(short_url)
        return

    click.echo("Short url: " + click.style(short_url, fg="green"))
    click.echo(f"Redirects to: {response['redirect_url']}")
    click.echo(f"Expires at: {datetime.fromtimestamp(response['expires_at'])}")
    if response["stats_is_public"]:
        click.echo("Stats is public")



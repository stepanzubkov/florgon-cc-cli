"""
    Pastes management command.
"""
from datetime import datetime

import click

from florgon_cc_cli.services.config import get_access_token
from florgon_cc_cli.services.paste import build_paste_open_url, create_paste


@click.group()
def paste():
    """
    Command that interacts with single paste or list.
    """


@paste.command()
@click.option("-o", "--only-url", is_flag=True, default=False, help="Outputs single url to paste.")
@click.option(
    "-d", "--do-not-save", is_flag=True, default=False, help="Do not save paste in local history."
)
@click.option(
    "-s",
    "--stats-is-public",
    is_flag=True,
    default=False,
    help="Make paste stats public. Auth required.",
)
@click.option(
    "-b",
    "--burn-after-read",
    is_flag=True,
    default=False,
    help="Deletes paste after first reading.",
)
@click.argument("text", type=str)
def create(
    only_url: bool, do_not_save: bool, text: str, stats_is_public: bool, burn_after_read: bool
):
    """Creates short url."""
    access_token = get_access_token()
    if stats_is_public and access_token is None:
        click.secho("Auth required for --stats-is-public flag!", fg="red", err=True)
        return

    success, response = create_paste(
        text,
        stats_is_public=stats_is_public,
        burn_after_read=burn_after_read,
        access_token=access_token,
    )
    if not success:
        click.secho(response["message"], err=True, fg="red")
        return

    short_url = build_paste_open_url(response["hash"])
    if only_url:
        click.echo(short_url)
        return

    click.echo("Short url: " + click.style(short_url, fg="green"))
    click.echo(f"Text: \n{response['text']}")
    if response["burn_after_read"]:
        click.secho("This paste will burn after reading!", fg="bright_yellow")
    click.echo(f"Expires at: {datetime.fromtimestamp(response['expires_at'])}")
    if response["stats_is_public"]:
        click.echo("Stats is public")

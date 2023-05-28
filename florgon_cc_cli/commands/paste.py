"""
    Pastes management command.
"""
from io import TextIOWrapper
from datetime import datetime
from typing import List, Optional

import click

from florgon_cc_cli.services.config import get_access_token
from florgon_cc_cli.services.paste import build_paste_open_url, create_paste, get_pastes_list
from florgon_cc_cli.services.files import concat_files


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
@click.option("-f", "--from-file", "from_files", type=click.File("r"), multiple=True, help="Read paste from file.")
@click.option("-t", "--text", type=str, help="Paste text.")
def create(
    only_url: bool,
    do_not_save: bool,
    stats_is_public: bool,
    burn_after_read: bool,
    text: Optional[str],
    from_files: List[TextIOWrapper],
):
    """Creates short url."""
    if from_files and text:
        click.secho("Pass --from-file or --text, but not both!", fg="red", err=True)
        return
    if not from_files and not text:
        click.secho("Pass --from-file or --text!", fg="red", err=True)
        return
    if from_files:
        text = concat_files(from_files)

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


@paste.command()
def list():
    """Prints a list of your pastes. Auth expired."""
    success, response = get_pastes_list(access_token=get_access_token())
    if not success:
        click.secho(response["message"], err=True, fg="red")
        return

    click.echo("Your pastes:")
    for paste in response:
        text_preview = paste["text"].split("\n")[0][:50] + "..."
        if paste["is_expired"]:
            click.secho(
                    f"{build_paste_open_url(paste['hash'])} - {text_preview} (expired)", fg="red"
            )
        else:
            click.echo(f"{build_paste_open_url(paste['hash'])} - {text_preview}")


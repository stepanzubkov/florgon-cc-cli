"""
    Pastes management command.
"""
from io import TextIOWrapper
from datetime import datetime
from typing import List, Optional

import click

from florgon_cc_cli.services.config import get_access_token
from florgon_cc_cli.services.paste import (
    build_paste_open_url,
    create_paste,
    get_pastes_list,
    request_hash_from_pastes_list,
    get_paste_info_by_hash,
    delete_paste_by_hash,
    extract_hash_from_paste_short_url,
)
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
@click.option(
    "-f",
    "--from-file",
    "from_files",
    type=click.File("r"),
    multiple=True,
    help="Read paste from file.",
)
@click.option("-t", "--text", type=str, help="Paste text.")
def create(
    only_url: bool,
    do_not_save: bool,
    stats_is_public: bool,
    burn_after_read: bool,
    text: Optional[str],
    from_files: List[TextIOWrapper],
):
    """Creates paste from text or file."""
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
@click.option(
    "-e", "--exclude-expired", is_flag=True, default=False, help="Do not show expired pastes."
)
def list(exclude_expired: bool):
    """Prints a list of your pastes. Auth expired."""
    success, response = get_pastes_list(access_token=get_access_token())
    if not success:
        click.secho(response["message"], err=True, fg="red")
        return

    click.echo("Your pastes:")
    for paste in response:
        # NOTE: This is temporary solution. Should be moved to cc-api.
        if paste["is_expired"] and exclude_expired:
            continue

        text_preview = paste["text"].split("\n")[0][:50] + "..."
        if paste["is_expired"]:
            click.secho(
                f"{build_paste_open_url(paste['hash'])} - {text_preview} (expired)", fg="red"
            )
        else:
            click.echo(f"{build_paste_open_url(paste['hash'])} - {text_preview}")


@paste.command()
@click.option("-s", "--short_url", type=str, help="Short url.")
@click.option("-o", "--only-text", is_flag=True, default=False, help="Prints only paste text.")
def read(short_url, only_text):
    """Prints text and info about paste."""
    if short_url:
        short_url_hash = extract_hash_from_paste_short_url(short_url)
    else:
        click.echo("Short url is not specified, requesting for list of your pastes.")
        short_url_hash = request_hash_from_pastes_list(access_token=get_access_token())

    success, response = get_paste_info_by_hash(short_url_hash)
    if not success:
        click.secho(response["message"], err=True, fg="red")
        return
    if only_text:
        click.echo("Text:\n" + response["text"].replace("\\n", "\n"))
        return
    click.echo(f"Expires at: {datetime.fromtimestamp(response['expires_at'])}")
    if response["stats_is_public"]:
        click.echo("Stats is public")
    if response["burn_after_read"]:
        click.secho("This paste will burn after reading!", fg="bright_yellow")
    click.echo("Text:\n" + response["text"].replace("\\n", "\n"))


@paste.command()
@click.option("-s", "--short-url", type=str, help="Short url.")
def delete(short_url: str):
    """
    Deletes paste. Auth Required.
    """
    if short_url:
        short_url_hash = extract_hash_from_paste_short_url(short_url)
    else:
        click.echo("Short url is not specified, requesting for list of your pastes.")
        short_url_hash = request_hash_from_pastes_list(access_token=get_access_token())

    success, *response = delete_paste_by_hash(
        hash=short_url_hash,
        access_token=get_access_token(),
    )
    if not success:
        click.secho(response[0]["message"], err=True, fg="red")
        return
    else:
        click.secho("Paste was successfully deleted!", fg="green")

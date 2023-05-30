"""
    Pastes management command.
"""
from io import TextIOWrapper
from datetime import datetime
from typing import List, Optional, Union, NoReturn

import click, re

from florgon_cc_cli.services.config import get_access_token
from florgon_cc_cli.services.paste import build_paste_open_url, create_paste, get_pastes_list, request_hash_from_urls_list, get_url_info_by_hash, delete_url_by_hash
from florgon_cc_cli.services.files import concat_files
from florgon_cc_cli import config


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
    click.echo(response)
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

def extract_hash_from_short_url(short_url: str) -> Union[str, NoReturn]:
    """
    Extracts hash from short url.
    :param str short_url: short url
    :rtype: Union[str, NoReturn]
    :return: url hash or exit application
    """
    short_url_hashes = re.findall(f"^{config.URL_PASTE_OPEN_PROVIDER}" + r"/([a-zA-Z0-9]{6})$", short_url)
    if not short_url_hashes:
        click.secho(
            f"Short url is invalid! It should be in form '{config.URL_PASTE_OPEN_PROVIDER}/xxxxxx'",
            err=True,
            fg="red",
        )
        click.get_current_context().exit(1)

    return short_url_hashes[0]


@paste.command()
@click.option('-s', 'short_url', type=str, help='short url')
@click.option('-o', '--only-text', is_flag=True, default=False, help='only text return', ) 
def read(short_url, only_text):
    """Read a paste"""
    if short_url:
        short_url_hash = extract_hash_from_short_url(short_url)
    else:
        click.echo("Short url is not specified, requesting for list of your urls.")
        short_url_hash = request_hash_from_urls_list()

    success, response = get_url_info_by_hash(short_url_hash)
    if not success:
        click.secho(response["message"], err=True, fg="red")
        return
    if not only_text:
        click.echo(f"Expires at: {datetime.fromtimestamp(response['expires_at'])}")
        if response["stats_is_public"]:
            click.echo("Stats is public")
        click.echo("Text:\n" + click.style(response["text"], bg='white', fg="blue"))
    else:
        click.echo("Text:\n" + click.style(response["text"], bg='white', fg="blue"))

@paste.command()
@click.option("-s", "--short-url", type=str, help="Short url.")
def delete(short_url: str):
    """
    Deletes paste. Auth Required.
    """
    if short_url:
        short_url_hash = extract_hash_from_short_url(short_url)
    else:
        click.echo("Short url is not specified, requesting for list of your urls.")
        short_url_hash = request_hash_from_urls_list()

    success, *response = delete_url_by_hash(
        hash=short_url_hash,
        access_token=get_access_token(),
    )
    if not success:
        click.secho(response[0]["message"], err=True, fg="red")
        return
    else:
        click.secho("Url was successfully deleted!", fg="green")

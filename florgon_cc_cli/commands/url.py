"""
    Single url commands.
"""
import click


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
    click.echo(f"Hello! only_url: {only_url}, do_not_save: {do_not_save}, long_url: {long_url}")

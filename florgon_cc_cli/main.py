"""
    Main module. Can be run like this:
    ```
    python main.py --help
    ```
"""
import click

from florgon_cc_cli.commands import url
from florgon_cc_cli.commands.login import login


@click.group()
def main():
    """Florgon CC CLI - url shortener and paste manager."""


main.add_command(url)
main.add_command(login)

if __name__ == "__main__":
    main()

"""
    Main module. Can be run like this:
    ```
    python main.py --help
    ```
"""
import click

from florgon_cc_cli.commands import url, login, logout


@click.group()
def main():
    """Florgon CC CLI - url shortener and paste manager."""


main.add_command(url)
main.add_command(login)
main.add_command(logout)

if __name__ == "__main__":
    main()

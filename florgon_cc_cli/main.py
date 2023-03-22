"""
    Main module. Can be run like this:
    ```
    python main.py --help
    ```
"""
import click

from commands import url


@click.group()
def main():
    """Florgon CC CLI - url shortener and paste manager."""


main.add_command(url)

if __name__ == "__main__":
    main()

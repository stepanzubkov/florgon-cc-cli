"""
    Main module. Can be run like this:
    ```
    python main.py --help
    ```
"""
import click

from florgon_cc_cli.commands import url, login, logout, host, config


@click.group()
@click.option("-D", "--debug", is_flag=True, default=False,
              help="Enable debug features like printing api responses.")
@click.pass_context
def main(ctx: click.Context, debug: bool):
    ctx.obj = {"DEBUG": debug}
    """Florgon CC CLI - url shortener and paste manager."""


main.add_command(url)
main.add_command(login)
main.add_command(logout)
main.add_command(host)
main.add_command(config)

if __name__ == "__main__":
    main()

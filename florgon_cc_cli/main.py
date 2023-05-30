"""
    Main module. Can be run like this:
    ```
    python main.py --help
    ```
"""
import click

from florgon_cc_cli.commands import url, login, logout, host, config, paste


@click.group()
@click.option(
    "-D",
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug features like printing api responses.",
)
@click.option(
    "-a", "--anonymous", is_flag=True, default=False, help="Do not use access token for request."
)
@click.pass_context
def main(ctx: click.Context, debug: bool, anonymous: bool):
    ctx.obj = {"DEBUG": debug, "ANONYMOUS": anonymous}
    """Florgon CC CLI - url shortener and paste manager."""


main.add_command(url)
main.add_command(login)
main.add_command(logout)
main.add_command(host)
main.add_command(config)
main.add_command(paste)

if __name__ == "__main__":
    main()

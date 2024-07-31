"""
Picasso commands group.
"""

import click
from tutorpicasso.commands.enable_private_packages import enable_private_packages
from tutorpicasso.commands.enable_themes import enable_themes
from tutorpicasso.commands.run_extra_commands import run_extra_commands

@click.group(help="Run picasso commands")
def picasso() -> None:
    """
    Main picasso command group.

    This command group provides functionality to run picasso commands.
    """


picasso.add_command(enable_private_packages)
picasso.add_command(run_extra_commands)
picasso.add_command(enable_themes)

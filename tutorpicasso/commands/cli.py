"""
Picasso commands group.
"""

import click

from tutorpicasso.commands.enable_private_packages import enable_private_packages
from tutorpicasso.commands.enable_themes import enable_themes
from tutorpicasso.commands.repository_validator import repository_validator
from tutorpicasso.commands.run_extra_commands import run_extra_commands
from tutorpicasso.commands.syntax_validator import syntax_validator


@click.group(help="Run picasso commands")
def picasso() -> None:
    """
    Main picasso command group.

    This command group provides functionality to run picasso commands.
    """


picasso.add_command(enable_themes)
picasso.add_command(enable_private_packages)
picasso.add_command(repository_validator)
picasso.add_command(syntax_validator)
picasso.add_command(run_extra_commands)

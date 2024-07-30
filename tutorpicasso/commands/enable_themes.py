"""
Picasso enable theme command.
"""

import subprocess

import click
from tutor import config as tutor_config

from tutorpicasso.picasso.themes.application.theme_enabler import ThemeEnabler
from tutorpicasso.picasso.themes.infraestructure.theme_git_repository import ThemeGitRepository


@click.command(name="enable-themes", help="Enable picasso themes")
def enable_themes() -> None:
    """
    Enable picasso themes.

    This function enables the themes specified in the `PICASSO_THEMES` configuration
    and applies them using the ThemeEnabler and ThemeGitRepository classes.
    """
    directory = subprocess.check_output("tutor config printroot", shell=True).\
        decode("utf-8").strip()
    config = tutor_config.load(directory)

    repository = ThemeGitRepository()
    enabler = ThemeEnabler(repository=repository)

    if config.get("PICASSO_THEMES"):
        for theme in config["PICASSO_THEMES"]:
            enabler(settings=theme, tutor_root=directory, tutor_config=config)

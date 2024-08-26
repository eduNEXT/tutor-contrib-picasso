import os
import subprocess
from typing import Any

import click
from tutor import config as tutor_config


@click.command(name="enable-themes", help="Enable picasso themes")
def enable_themes() -> None:
    """
    Enable picasso themes.

    This function enables the themes specified in the `PICASSO_THEMES` configuration
    and applies them using the ThemeEnabler and ThemeGitRepository classes.
    """
    context = click.get_current_context().obj
    tutor_root = context.root
    tutor_conf = tutor_config.load(tutor_root)

    if not tutor_conf.get("PICASSO_THEMES"):
        return

    # We use `type: ignore` for the `tutor_conf` object
    # because it comes from the Tutor framework.
    # We are not handle type errors related to this object.
    for theme in tutor_conf["PICASSO_THEMES"]:  # type: ignore
        if not {"name", "repo", "version"}.issubset(theme.keys()):  # type: ignore
            raise click.ClickException(
                f"{theme} is missing one or more required keys: "
                "'name', 'repo', 'version'"
            )

        theme_path = f'{tutor_root}/env/build/openedx/themes/{theme["name"]}'  # type: ignore
        if os.path.isdir(theme_path):
            subprocess.call(["rm", "-rf", theme_path])

        subprocess.call(
            ["git", "clone", "-b", theme["version"], theme["repo"], theme_path],  # type: ignore
        )

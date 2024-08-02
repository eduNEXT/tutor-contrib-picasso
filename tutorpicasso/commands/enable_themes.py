import os
import subprocess

import click
from tutor import config as tutor_config


@click.command(name="enable-themes", help="Enable picasso themes")
def enable_themes() -> None:
    """
    Enable picasso themes.

    This function enables the themes specified in the `PICASSO_THEMES` configuration
    and applies them using the ThemeEnabler and ThemeGitRepository classes.
    """
    tutor_root = (
        subprocess.check_output("tutor config printroot", shell=True)
        .decode("utf-8")
        .strip()
    )
    config = tutor_config.load(tutor_root)

    if config.get("PICASSO_THEMES"):
        for theme in config["PICASSO_THEMES"]:
            try:
                if not {"name", "repo", "version"}.issubset(theme.keys()):
                    raise KeyError(
                        f"{theme} is missing one or more required keys: "
                        "'name', 'repo', 'version'"
                    )

                theme_path = f'{tutor_root}/env/build/openedx/themes/{theme["name"]}'
                if os.path.isdir(theme_path):
                    subprocess.call(["rm", "-rf", theme_path])

                subprocess.call(
                    ["git", "clone", "-b", theme["version"], theme["repo"], theme_path],
                )
            except KeyError as e:
                raise click.ClickException(f"Error: {str(e)}")

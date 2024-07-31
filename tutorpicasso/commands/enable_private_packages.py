import os
import click
import subprocess
from tutor import config as tutor_config



@click.command(name="enable-private-packages", help="Enable picasso private packages")
def enable_private_packages():
    """
    Enable private packages command.

    This command enables picasso private packages by cloning the packages and
    defining them as private.

    Raises:
        Exception: If an error occurs during the cloning or defining process.
    """
    tutor_root = subprocess.check_output("tutor config printroot", shell=True).\
        decode("utf-8").strip()
    config = tutor_config.load(tutor_root)
    packages = get_picasso_packages(config)
    for package, info in packages.items():
        try:
            if not {"name", "repo", "version"}.issubset(info):
                raise KeyError(f"{package} is missing one of the required keys: 'name', 'repo', 'version'")

            if os.path.isdir(f'{tutor_root}/{info["name"]}'):
                subprocess.call(
                    [
                        "rm", "-rf", f'{tutor_root}/{info["name"]}'
                    ]
                )

            subprocess.call(
                [
                    "git", "clone", "-b",
                    info["version"], info["repo"]
                ],
                cwd=tutor_root
            )
            subprocess.call(
                [
                    "tutor", "mounts", "add", f'{tutor_root}/{info["name"]}'
                ]
            )

        except KeyError as e:
            raise click.ClickException(str(e))

def get_picasso_packages(settings) -> dict:
    """
    Get the distribution packages from the provided settings.

    Args:
        settings (dict): The tutor configuration settings.

    Returns:
        dict: A dictionary of distribution packages, where the keys are package names
        and the values are package details.
    """
    picasso_packages = {key: val for key,
                       val in settings.items() if key.endswith("_DPKG") and val != 'None'}
    return picasso_packages

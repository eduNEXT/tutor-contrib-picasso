import os
import subprocess
from typing import Any, Dict

import click
from packaging.version import Version
from tutor import config as tutor_config
from tutor.__about__ import __version__ as tutor_version


@click.command(name="enable-private-packages", help="Enable picasso private packages")
def enable_private_packages() -> None:
    """
    Enable private packages command.

    This command enables picasso private packages by cloning the packages and
    defining them as private.

    Raises:
        Exception: If an error occurs during the cloning or defining process.
    """
    tutor_root = (
        subprocess.check_output("tutor config printroot", shell=True)
        .decode("utf-8")
        .strip()
    )
    tutor_version_obj = Version(tutor_version)
    # Define Quince version as the method for installing private packages changes from this version
    quince_version_obj = Version("v17.0.0")
    # Use these specific paths as required by Tutor < Quince
    private_requirements_root = f"{tutor_root}/env/build/openedx/requirements"
    private_requirements_txt = f"{private_requirements_root}/private.txt"
    config = tutor_config.load(tutor_root)
    packages = get_picasso_packages(config)

    # Create necessary files and directories if they don't exist
    if not os.path.exists(private_requirements_root):
        os.makedirs(private_requirements_root)
    if (
        not os.path.exists(private_requirements_txt)
        and tutor_version_obj < quince_version_obj
    ):
        with open(private_requirements_txt, "w") as file:
            file.write("")

    for package, info in packages.items():
        try:
            if not {"name", "repo", "version"}.issubset(info):
                raise KeyError(
                    f"{package} is missing one of the required keys: 'name', 'repo', 'version'"
                )

            if os.path.isdir(f'{private_requirements_root}/{info["name"]}'):
                subprocess.call(
                    ["rm", "-rf", f'{private_requirements_root}/{info["name"]}']
                )

            subprocess.call(
                ["git", "clone", "-b", info["version"], info["repo"]],
                cwd=private_requirements_root,
            )

            if tutor_version_obj < quince_version_obj:
                echo_command = (
                    f'echo "-e ./{info["name"]}/" >> {private_requirements_txt}'
                )
                subprocess.call(echo_command, shell=True)
            else:
                subprocess.call(
                    [
                        "tutor",
                        "mounts",
                        "add",
                        f'{private_requirements_root}/{info["name"]}',
                    ]
                )

        except KeyError as e:
            raise click.ClickException(str(e))


def get_picasso_packages(settings: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Get the distribution packages from the provided settings.

    Args:
        settings (dict): The tutor configuration settings.

    Returns:
        dict: A dictionary of distribution packages, where the keys are package names
        and the values are package details.
    """
    picasso_packages = {
        key: val
        for key, val in settings.items()
        if key.endswith("_DPKG") and val != "None"
    }
    return picasso_packages

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
        Exception: If there is not enough information to clone the repo.
    """
    context = click.get_current_context().obj
    tutor_root = context.root
    tutor_conf = tutor_config.load(tutor_root)

    tutor_version_obj = Version(tutor_version)
    # Define Quince version as the method for installing private packages changes from this version
    quince_version_obj = Version("v17.0.0")

    # Use these specific paths as required by Tutor < Quince
    private_requirements_root = f"{tutor_root}/env/build/openedx/requirements"
    packages = get_picasso_packages(tutor_conf)

    # Create necessary directory if it doesn't exist
    if not os.path.exists(private_requirements_root):
        os.makedirs(private_requirements_root)

    for package, info in packages.items():
        if not {"name", "repo", "version"}.issubset(info):
            raise click.ClickException(
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
            private_requirements_txt = f"{private_requirements_root}/private.txt"
            _enable_private_packages_before_quince(info, private_requirements_txt)
        else:
            _enable_private_packages(info, private_requirements_root)


def _enable_private_packages_before_quince(
    info: Dict[str, str], private_requirements_txt: str
) -> None:
    """
    Copy the package name in the private.txt file to ensure that packages are added in the build process for Tutor versions < Quince.

    Args:
        info (Dict[str, str]): A dictionary containing metadata about the package. Expected to have a "name" key.
        private_requirements_txt (str): The file path to `private.txt`, which stores the list of private packages to be included in the build.
    """

    # Create necessary file if it doesn't exist
    if not os.path.exists(private_requirements_txt):
        with open(private_requirements_txt, "w") as file:
            file.write("")

    echo_command = f'echo "-e ./{info["name"]}/" >> {private_requirements_txt}'
    subprocess.call(echo_command, shell=True)


def _enable_private_packages(
    info: Dict[str, str], private_requirements_root: str
) -> None:
    """
    Use the tutor mounts method to ensure that packages are added in the build process.

    Args:
        info (Dict[str, str]): A dictionary containing metadata about the package. Expected to have a "name" key.
        private_requirements_root (str): The root directory where private packages are stored.
    """
    subprocess.call(
        [
            "tutor",
            "mounts",
            "add",
            f'{private_requirements_root}/{info["name"]}',
        ]
    )


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
        key: val for key, val in settings.items() if key.endswith("_DPKG") and val
    }
    return picasso_packages

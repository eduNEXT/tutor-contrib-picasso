import os
import subprocess
from typing import Any, Dict

import click
from packaging.version import Version
from tutor import config as tutor_config
from tutor.__about__ import __version__ as tutor_version
from tutor import utils as tutor_utils
from tutor import fmt as tutor_fmt


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

    private_requirements_path = f"{tutor_root}/env/build/openedx/requirements"
    packages = get_picasso_packages(tutor_conf)

    if not os.path.exists(private_requirements_path):
        os.makedirs(private_requirements_path)

    for package, info in packages.items():
        if not {"name", "repo", "version"}.issubset(info):
            raise click.ClickException(
                f"{package} is missing one of the required keys: 'name', 'repo', 'version'"
            )

        requirement_path = f'{private_requirements_path}/{info["name"]}'
        if os.path.isdir(requirement_path):
            tutor_utils.execute("rm", "-rf", requirement_path)

        tutor_utils.execute(
            "git", "clone", "-b", info["version"], info["repo"], requirement_path
        )

        handle_private_requirements_by_tutor_version(info, private_requirements_path)


def handle_private_requirements_by_tutor_version(
    info: Dict[str, str], private_requirements_path: str
) -> None:
    """
    Handle the private requirements based on the Tutor version.

    Args:
        info (Dict[str, str]): A dictionary containing metadata about the requirement. Expected to have a "name" key.
        private_requirements_path (str): The directory path to store the private requirements.
    """
    tutor_version_obj = Version(tutor_version)
    quince_version_obj = Version("v17.0.0")

    if tutor_version_obj < quince_version_obj:
        private_txt_path = f"{private_requirements_path}/private.txt"
        _enable_private_requirements_before_quince(info, private_txt_path)
    else:
        _enable_private_requirements_latest(info, private_requirements_path)


def _enable_private_requirements_before_quince(
    info: Dict[str, str], private_requirements_txt: str
) -> None:
    """
    Copy the requirement name in the private.txt file to ensure that requirements are added in the build process for Tutor versions < Quince.

    Args:
        info (Dict[str, str]): A dictionary containing metadata about the requirement. Expected to have a "name" key.
        private_requirements_txt (str): The file path to `private.txt`, which stores the list of private requirements to be included in the build.
    """
    if not os.path.exists(private_requirements_txt):
        with open(private_requirements_txt, "w") as file:
            file.write("")

    echo_command = f'echo "-e ./{info["name"]}/" >> {private_requirements_txt}'
    subprocess.call(echo_command, shell=True)
    click.echo(tutor_fmt.command(echo_command))


def _enable_private_requirements_latest(
    info: Dict[str, str], private_requirements_path: str
) -> None:
    """
    Use the tutor mounts method to ensure that requirements are added in the build process.

    Args:
        info (Dict[str, str]): A dictionary containing metadata about the requirement. Expected to have a "name" key.
        private_requirements_path (str): The root directory where private requirements are stored.
    """
    tutor_utils.execute(
        "tutor", "mounts", "add", f'{private_requirements_path}/{info["name"]}'
    )


def get_picasso_packages(settings: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Get the distribution packages from the provided settings.

    Args:
        settings (dict): The tutor configuration settings.

    Returns:
        A dictionary of distribution packages, where the keys are package names
        and the values are package details.
    """
    picasso_packages = {
        key: val
        for key, val in settings.items()
        if key.startswith("PICASSO_") and key.endswith("_DPKG") and val
    }
    return picasso_packages

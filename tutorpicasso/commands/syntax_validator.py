"""
Picasso config syntax validator command.
"""

import subprocess

import click

from tutorpicasso.picasso.share.domain.config_extra_files_requirements_setting import ConfigExtraFilesRequirementsSetting
from tutorpicasso.picasso.share.domain.config_extra_pip_requirements_setting import ConfigExtraPipRequirementsSetting
from tutorpicasso.picasso.share.domain.config_extra_setting import ConfigExtraSetting
from tutorpicasso.picasso.share.domain.config_packages_setting import ConfigPackagesSetting
from tutorpicasso.picasso.share.domain.config_themes_setting import ConfigThemesSetting
from tutorpicasso.picasso.syntax_validator.application.config_syntax_validator import ConfigSyntaxValidator
from tutorpicasso.picasso.syntax_validator.infrastructure.config_repository import ConfigRepository


@click.command(name="syntax-validator", help="Syntax validator")
def syntax_validator() -> None:
    """
    Command to perform syntax validation on the configuration.

    This command loads the Tutor configuration, validates it using the
    ConfigSyntaxValidator, and displays the validation result.
    """
    file_path = subprocess.check_output("tutor config printroot", shell=True).decode("utf-8").strip()

    config_settings = [
        ConfigExtraFilesRequirementsSetting,
        ConfigExtraPipRequirementsSetting,
        ConfigExtraSetting,
        ConfigPackagesSetting,
        ConfigThemesSetting,
    ]
    repository = ConfigRepository(config_settings)

    syntax_validator = ConfigSyntaxValidator(repository)
    is_valid = syntax_validator.execute(file_path)

    if is_valid:
        click.echo("Success validation")
    else:
        click.echo("Failed validation. Check settings")

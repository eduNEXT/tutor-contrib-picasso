"""
Picasso run extra commands command.
"""

import subprocess

import click
from tutor import config as tutor_config

from tutorpicasso.picasso.extra_commands.application.commands_runner import CommandsRunner
from tutorpicasso.picasso.extra_commands.infrastructure.tutor_commands import TutorCommandManager


@click.command(name="run-extra-commands", help="Run tutor commands")
def run_extra_commands():
    """
    This command runs tutor commands defined in PICASSO_EXTRA_COMMANDS
    """
    directory = (
        subprocess.check_output("tutor config printroot", shell=True)
        .decode("utf-8")
        .strip()
    )
    config = tutor_config.load(directory)
    picasso_extra_commands = config.get("PICASSO_EXTRA_COMMANDS", None)

    tutor_commands_manager = TutorCommandManager()
    run_tutor_command = CommandsRunner(commands_manager=tutor_commands_manager, commands=picasso_extra_commands)

    if picasso_extra_commands:
        for command in picasso_extra_commands:
            run_tutor_command(command=command)

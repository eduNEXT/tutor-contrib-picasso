
import click
import subprocess
from tutor import config as tutor_config
import re
# Was necessary to use this for compatibility with Python 3.8
from typing import List

COMMAND_CHAINING_OPERATORS = ["&&", "&", "||", "|", ";"]

@click.command(name="run-extra-commands", help="Run tutor commands")
def run_extra_commands():
    """
    This command runs tutor commands defined in PICASSO_EXTRA_COMMANDS
    """
    tutor_root = subprocess.check_output("tutor config printroot", shell=True).\
        decode("utf-8").strip()
    config = tutor_config.load(tutor_root)
    picasso_extra_commands = config.get("PICASSO_EXTRA_COMMANDS", None)
    if picasso_extra_commands is not None:
        validate_commands(picasso_extra_commands)
        for command in picasso_extra_commands:
                run_command(command)


def validate_commands(commands: List[str]):
    """
    Takes all the extra commands sent through config.yml and verifies that
    all the commands are correct before executing them

    Args:
        commands (list[str] | None): The commands sent through DISTRO_EXTRA_COMMANDS in config.yml
    """
    splitted_commands = [
        split_string(command, COMMAND_CHAINING_OPERATORS) for command in commands
    ]
    flat_commands_array = sum(splitted_commands, [])

    invalid_commands = []
    misspelled_commands = []
    for command in flat_commands_array:
        if "tutor" not in command.lower():
            if find_tutor_misspelled(command):
                misspelled_commands.append(command)
            else:
                invalid_commands.append(command)

        if invalid_commands or misspelled_commands:
            error_message = (
            f"Found some issues with the commands:\n\n"
            f"{'=> Invalid commands: ' if invalid_commands else ''}"
            f"{', '.join(invalid_commands) if invalid_commands else ''}\n"
            f"{'=> Misspelled commands: ' if misspelled_commands else ''}"
            f"{', '.join(misspelled_commands) if misspelled_commands else ''}\n"
            f"Take a look at the official Tutor commands: "
            f"https://docs.tutor.edly.io/reference/cli/index.html"
            )
            raise click.ClickException(error_message)

def run_command(command: str):
    """
    Run an extra command.

    This method runs the extra command provided.

    Args:
            command (str): Tutor command.
    """
    try:
        with subprocess.Popen(
            command,
            shell=True,
            executable="/bin/bash",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            ) as process:

            # It is sent a 'y' to say 'yes' on overriding the existing folders
            stdout, stderr = process.communicate(input="y")

            if process.returncode != 0 or "error" in stderr.lower():
                raise subprocess.CalledProcessError(
                    process.returncode, command, output=stdout, stderr=stderr
                )

            # This print is left on purpose to show the command output
            click.echo(stdout)

    except subprocess.CalledProcessError as error:
        raise click.ClickException(error)


def find_tutor_misspelled(command: str):
    """
    This function takes a command and looks if it has the word 'tutor' misspelled

    Args:
        command (str): Command to be reviewed

    Return:
        If its found the word 'tutor' misspelled is returned True
    """
    return re.match(r"[tT](?:[oru]{3}|[oru]{2}[rR]|[oru]u?)", command)


def create_regex_from_array(arr: List[str]):
    """
    This functions compiles a new regex turning taking care of
    escaping special characters

    Args:
        arr (list[str]): String that would be used to create a new regex

    Return:
        A new compiled regex pattern that can be used for comparisons
    """
    escaped_arr = [re.escape(item) for item in arr]
    regex_pattern = "|".join(escaped_arr)
    return re.compile(regex_pattern)


def split_string(string: str, split_by: List[str]):
    """
    Takes a string that is wanted to be split according to some
    other strings received in a list

    Args:
        string (str): String that will be split
        split_by (list[str]): Array of strings which will be used to split the string

    Return:
        The string split into an array
    """
    return re.split(create_regex_from_array(split_by), string)

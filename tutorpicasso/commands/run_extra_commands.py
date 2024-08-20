import re
import subprocess
from itertools import chain

# Was necessary to use this for compatibility with Python 3.8
from typing import Any, List

import click
from tutor import config as tutor_config

COMMAND_CHAINING_OPERATORS = ["&&", "&", "||", "|", ";"]


@click.command(name="run-extra-commands", help="Run tutor commands")
def run_extra_commands() -> None:
    """
    This command runs tutor commands defined in PICASSO_EXTRA_COMMANDS
    """
    context = click.get_current_context().obj
    tutor_conf = tutor_config.load(context.root)

    picasso_extra_commands: Any = tutor_conf.get("PICASSO_EXTRA_COMMANDS", None)

    if not picasso_extra_commands:
        return

    error_message = validate_commands(picasso_extra_commands)
    if error_message:
        raise click.ClickException(error_message)

    list(map(run_command, picasso_extra_commands))


def validate_commands(commands: Any) -> str:
    """
    Takes all the extra commands sent through config.yml and verifies that
    all the commands are correct before executing them

    Args:
        commands (list[str] | None): The commands sent through PICASSO_EXTRA_COMMANDS in config.yml
    """
    splitted_commands = [
        split_string(command, COMMAND_CHAINING_OPERATORS) for command in commands
    ]
    flat_commands_list: chain[str] = chain.from_iterable(splitted_commands)

    invalid_commands = []
    misspelled_commands = []
    for command in flat_commands_list:
        if "tutor" not in command.lower():
            if find_tutor_misspelled(command):
                misspelled_commands.append(command)
            else:
                invalid_commands.append(command)

        error_message = ""

        if invalid_commands:
            error_message += (
                f"Found some issues with the commands:\n\n"
                f"=> Invalid commands: {', '.join(invalid_commands)}\n"
            )

        if misspelled_commands:
            error_message += (
                f"=> Misspelled commands: {', '.join(misspelled_commands)}\n"
            )

        if error_message:
            error_message += (
                "Take a look at the official Tutor commands: "
                "https://docs.tutor.edly.io/reference/cli/index.html"
            )
            return error_message
    return ""


def run_command(command: str) -> None:
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

            stdout, stderr = process.communicate()

            if process.returncode != 0 or "error" in stderr.lower():
                raise subprocess.CalledProcessError(
                    process.returncode, command, output=stdout, stderr=stderr
                )

            click.echo(stdout)

    except subprocess.CalledProcessError as error:
        raise click.ClickException(str(error))


def find_tutor_misspelled(command: str) -> bool:
    """
    Look for misspelled occurrences of the word `tutor` in a given string. E.g. ...

    Args:
        command (str): string to be reviewed.

    Return:
        True if any misspelled occurrence is found, False otherwise.

    Args:
        command (str): Command to be reviewed

    Return:
        If its found the word 'tutor' misspelled is returned True
    """
    return bool(re.match(r"[tT](?:[oru]{3}|[oru]{2}[rR]|[oru]u?)", command))


def create_regex_from_list(special_chars: List[str]) -> re.Pattern[str]:
    """
    Compile a new regex and escape special characters in the given string.
    escaping special characters

    Args:
        special_chars (list[str]): String that would be used to create a new regex

    Return:
        A new compiled regex pattern that can be used for comparisons
    """
    escaped_special_chars = list(map(re.escape, special_chars))  # type: ignore
    regex_pattern = "|".join(escaped_special_chars)  # type: ignore
    return re.compile(regex_pattern)


def split_string(string: str, split_by: List[str]) -> List[str]:
    """
    Split strings based on given patterns.

    Args:
        string (str): string to be split
        split_by (list[str]): patterns to be used to split the string

    Return:
        The string split into a list
    """
    return re.split(create_regex_from_list(split_by), string)

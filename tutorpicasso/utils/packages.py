"""
Module: tutorpicasso.utils.packages
This module provides utility functions to handle distribution packages in the tutor configuration settings.
"""


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


def get_public_picasso_packages(settings) -> dict:
    """
    Get the public distribution packages from the provided settings.

    Args:
        settings (dict): The tutor configuration settings.

    Returns:
        dict: A dictionary of public distribution packages, where the keys are package names
        and the values are package details.
    """
    picasso_packages = get_picasso_packages(settings)
    public_packages = {key: val for key,
                       val in picasso_packages.items() if not val["private"]}
    return public_packages


def get_private_picasso_packages(settings) -> dict:
    """
    Get the private distribution packages from the provided settings.

    Args:
        settings (dict): The tutor configuration settings.

    Returns:
        dict: A dictionary of private distribution packages, where the keys are package names
        and the values are package details.
    """
    picasso_packages = get_picasso_packages(settings)
    private_packages = {key: val for key,
                        val in picasso_packages.items() if val["private"]}
    return private_packages

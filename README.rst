Picasso `Tutor`_ Plugin
#########################

|Maintainance Badge| |Test Badge|

.. |Maintainance Badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
   :alt: Maintainance Status
.. |Test Badge| image:: https://img.shields.io/github/actions/workflow/status/edunext/tutor-contrib-picasso/.github%2Fworkflows%2Ftests.yml?label=Test
   :alt: GitHub Actions Workflow Test Status

Picasso is a `Tutor`_ plugin that simplifies pre-build processes, such as preparing Docker images with private requirements, executing commands before the build, and adding themes. Everything is managed through commands, making it easy to integrate into automated environments.

This plugin is based on https://github.com/eduNEXT/tutor-contrib-edunext-distro


Installation
************

.. code-block:: bash

    pip install git+https://github.com/eduNEXT/tutor-contrib-picasso

Usage
*****

.. code-block:: bash

    # To enable the plugin
    tutor plugins enable picasso

    # Show help
    tutor picasso -h

    # Enable themes
    tutor picasso enable-themes

    # Enable private packages
    tutor picasso enable-private-packages

    # Run Tutor commands
    tutor picasso run-extra-commands 

.. note::

    Remember to run these commands before build your images if they are needed.


Compatibility notes
*******************

This plugin was tested from Palm release.

About the commands
*******************

Enable Private Packages
^^^^^^^^^^^^^^^^^^^^^^^^

This command allows the installation of private Open edX Django apps. It clones the private repository and, through the ``tutor mounts`` command, adds it to the Dockerfile for inclusion in the build process. The input it takes is:

.. code-block:: yaml
    PICASSO_<YOUR_PACKAGE_NAME>_DPKG:
    name: <your_package_name>
    repo: <your SSH URL for cloning the repo. e.g., git@github.com:yourorg/package.git>
    version: <your branch, tag o release for cloning. e.g., v5.2.0>

.. note::

    It is needed to use the SSH URL to clone private packages.

.. warning::

    For the mount to work correctly and include the package in the Dockerfile, it must be added to a tutor filter ``MOUNTED_DIRECTORIES``. By default, Picasso adds ``eox-*`` packages. If you need to add another private package, don't forget to include this configuration in a Tutor plugin.

    .. code-block:: python

        hooks.Filters.MOUNTED_DIRECTORIES.add_items(
            [
                ("openedx", "<your_package_name>"),
            ]
        )


.. note::

    If you want to use public packages, we recommend using the ``OPEN_EDX_EXTRA_PIP_REQUIREMENTS`` variable in the ``config.yml`` of your Tutor environment.


Enable Themes
^^^^^^^^^^^^^^

This command clones your theme repository into the folder that Tutor uses for themes. Documentation available at `Installing custom theme`_ tutorial. The input it takes is:

.. code-block:: yaml
    PICASSO_THEMES:
    - name: <your_theme_name>
      repo: <your SSH URL for cloning the repo. e.g., git@github.com:yourorg/theme.git>
      version: <your branch, tag o release for cloning. e.g., edunext/redwood.master>
    - name: <another_theme_name>
      repo: <your SSH URL for cloning the repo. e.g., git@github.com:yourorg/another_theme.git>
      version: <your branch, tag o release for cloning. e.g., edunext/redwood.blue>

.. note::

    If your theme repository is public, you can also use the HTTPS URL in ``repo``.

.. note::

    Don't forget to add extra configurations in a Tutor plugin if your theme requires it.


Run Extra Commands
^^^^^^^^^^^^^^^^^^^

This command allows you to run a list of Tutor commands. These commands are executed in bash and, for security reasons, are restricted to running only Tutor commands. The input it takes is:

.. code-block:: yaml
    PICASSO_EXTRA_COMMANDS:
    - <A tutor command. e.g., tutor plugins index add X>
    - <A tutor command. e.g., tutor plugins install mfe>
    - <A tutor command. e.g., tutor picasso enable-themes>
    - <A tutor command. e.g., tutor config save>
    .
    .
    .

License
*******

This software is licensed under the terms of the AGPLv3.


.. _Tutor: https://docs.tutor.edly.io
.. _Installing custom theme: https://docs.tutor.edly.io/tutorials/theming.html#theming
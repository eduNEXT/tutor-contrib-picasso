Picasso `Tutor`_ Plugin
#########################

|Maintainance Badge| |Test Badge|

.. |Maintainance Badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
   :alt: Maintainance Status
.. |Test Badge| image:: https://img.shields.io/github/actions/workflow/status/edunext/tutor-contrib-picasso/.github%2Fworkflows%2Ftests.yml?label=Test
   :alt: GitHub Actions Workflow Test Status

Picasso is a `Tutor`_ plugin that streamlines and automates complex pre-build tasks into a cohesive command. 

Current features include:

- Adding private requirements: install private packages or dependencies in edx-platform.
- Executing a bundle of commands: run multiple commands in a specific order with a single command.
- Adding themes: manage custom themes to personalize Open edX.

This plugin is based on https://github.com/eduNEXT/tutor-contrib-edunext-distro


Installation
************

.. code-block:: bash

    pip install git+https://github.com/eduNEXT/tutor-contrib-picasso

Enable the plugin
******************

.. code-block:: bash

    # To enable the plugin
    tutor plugins enable picasso

    # Show the picasso commands
    tutor picasso -h


.. note::

    Please remember to run these commands before you build your images.


Compatibility notes
*******************

This plugin was tested from Olive release.

Usage
*******

Enable Private Packages
^^^^^^^^^^^^^^^^^^^^^^^^

To enable the installation of private Open edX Django apps, follow these steps:

1. Add configuration to the configuration file

First, add the necessary configuration in your Tutor environment's ``config.yml`` file:

.. code-block:: yaml
    PICASSO_<YOUR_PACKAGE_NAME>_DPKG:
    name: <your_package_name>
    repo: <your SSH URL for cloning the repo. e.g., git@github.com:yourorg/package.git>
    version: <your branch, tag o release for cloning. e.g., v5.2.0>

.. note::

    It is needed to use the SSH URL to clone private packages.

2. Save the configuration with ``tutor config save``

3. Run the enable command 

Next, run the following command to enable private packages:

.. code-block:: bash

    # Enable private packages
    tutor picasso enable-private-packages


This command allows the installation of private Open edX Django apps. It clones the private repository and, through the ``tutor mounts`` command, adds it to the Dockerfile for inclusion in the build process.

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

To enable themes in your Tutor environment, follow these steps:

1. Add configuration to the configuration file

First, add the necessary configuration in your Tutor environment's ``config.yml`` file:

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

2. Save the configuration with ``tutor config save``

3. Run the enable command

.. code-block:: bash

    # Enable themes
    tutor picasso enable-themes

This command clones your theme repository into the folder that Tutor uses for themes. Documentation available at `Installing custom theme`_ tutorial.

.. note::

    Don't forget to add extra configurations in a Tutor plugin if your theme requires it.


Run Extra Commands
^^^^^^^^^^^^^^^^^^^

To execute a list of Tutor commands in your Tutor environment, follow these steps:

1. Add configuration to the configuration file

First, add the necessary configuration in your Tutor environment's ``config.yml`` file:

.. code-block:: yaml
    PICASSO_EXTRA_COMMANDS:
    - <A tutor command. e.g., tutor plugins index add X>
    - <A tutor command. e.g., tutor plugins install mfe>
    - <A tutor command. e.g., tutor picasso enable-themes>
    - <A tutor command. e.g., tutor config save>
    .
    .
    .

2. Save the configuration with ``tutor config save``

3. Run the following command

.. code-block:: bash

    # Run Tutor commands
    tutor picasso run-extra-commands

This command allows you to run a list of Tutor commands. These commands are executed in bash and, for security reasons, are restricted to running only Tutor commands.


License
*******

This software is licensed under the terms of the AGPLv3.


.. _Tutor: https://docs.tutor.edly.io
.. _Installing custom theme: https://docs.tutor.edly.io/tutorials/theming.html#theming
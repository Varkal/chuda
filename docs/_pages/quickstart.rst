Quickstart
=================================

.. toctree::
    :hidden:

Eager to get started? This page gives a good introduction in how to get started with chuda.

First, make sure that:

* chuda is :doc:`installed <./install>`
* chuda is up-to-date

Let’s get started with some simple examples.

Hello World
-----------

Create an app with chuda is very simple

.. code-block:: python

    from chuda import App, autorun

    @autorun() # Equivalent to if __name__ == "__main__"
    class HelloWorldApp(App):
        def main(self):
            self.logger.info("Hello Word")




Parse a config file
-------------------

Chuda will handle for you the parsing of a configuration file

For example, with this configuration file:


.. code-block:: ini

    # ./config.ini

    [hello]
    name = John

This code will parse it automatically:

.. code-block:: python

    from chuda import App, autorun

    @autorun()
    class ConfigApp(App):
        config_path = ["./config.ini", "../config.ini"]

        def main(self):
            self.logger.info("Hello {}".format(self.config["hello"]["name"]))

chuda can handle ini (default), json and yaml files (only if `pyyaml <https://pyyaml.org/>`_ is installed).
You must specified which parser will be used with the :attr:`~chuda.app.App.config_parser` attribute

As you can see, :attr:`~chuda.app.App.config_path` is a list.
Chuda will try to load each file in the order in which they have been declared until it find one that exists.

Handle arguments
----------------

Chuda gives you a declarative interface to add options and parameters to your applications

.. code-block:: python

    from chuda import App, autorun, Option, Parameter

    @autorun()
    class ArgumentsApp(App):

        arguments = [
            Option(["--language"], default="en", choices=["en", "fr"]),
            Option(["--polite", "-p"], action="store_true"),
            Parameter("name"),
        ]

        def main(self):
            salutation = ""

            if self.arguments.language == "en":
                salutation = "Hello " if self.arguments.polite else "Hi "
            elif self.arguments.language == "fr":
                salutation = "Bonjour " if self.arguments.polite else "Salut "

            salutation += self.arguments.name

            self.logger.info(salutation)

An :class:`~chuda.arguments.Option` represent an UNIX style option ("e.g: git commit **-m** stuff")

A :class:`~chuda.arguments.Parameter` represent a simple parameter ("e.g: git checkout **stuff**")

Both takes the same parameters as the :meth:`~argparse.ArgumentParser.add_argument` method.
Additionaly, they take a :attr:`~chuda.arguments.Argument.completer` attribute use by
`argcomplete <https://argcomplete.readthedocs.io/en/latest/>`_

By default, chuda proposes three basic options :

* ``-q`` / ``--quiet`` : The logger stop logging
* ``-v`` / ``--verbose`` : The logging level is lowered to debug
* ``--version`` : print the content of the :attr:`~chuda.app.App.version` attribute and exit

Create subcommands
------------------

Chuda gives you a very simple way to create subcommands in your
application by defining :class:`~chuda.commands.Command` subclasses

.. code-block:: python

    from chuda import App, autorun, Command

    # Should be split in mutiple files

    class FirstCommand(Command):
        command_name = "first"
        description = "this is the first command"

        def main(self):
            self.logger.info("first from {}".format(self.app.app_name))


    class SecondCommand(Command):
        command_name = "second"
        description = "this is the second command"

        def main(self):
            self.logger.info("second from {}".format(self.app.app_name))


    @autorun()
    class SubCommandsApp(App):
        app_name = "my_app"

        subcommands = [
            FirstCommand,
            SecondCommand
        ]

:attr:`~chuda.app.App.subcommands` is transformed to a dictionnary at runtime. So, if you need to call a subcommand from
an other subcommand :

.. code-block:: python

    from chuda import App, autorun, Command

    # Should be split in mutiple files

    class FirstCommand(Command):
        command_name = "first"
        description = "this is the first command"

        def main(self):
            self.logger.info("first from {}".format(self.app.app_name))


    class SecondCommand(Command):
        command_name = "second"
        description = "this is the second command"

        def main(self):
            self.app.subcommands["first"].run()


    @autorun()
    class SubCommandsApp(App):
        app_name = "my_app"

        subcommands = [
            FirstCommand,
            SecondCommand
        ]

Run shell commands
------------------

Chuda gives you a simple interface to interop with other shell utils

.. code-block:: python

    from chuda import App, autorun

    @autorun()
    class ShellSyncApp(App):
        def main(self):
            process = self.shell.run("ls")
            self.logger.info(process.output)


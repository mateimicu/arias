"""This module contains the entry point for the command line application."""

import argparse
import sys

from oslo_log import log as logging

from arias.cli import base as cli_base
from arias.cli import commands as cli_commands
from arias import config

CONFIG = config.CONFIG


class AriasCli(cli_base.Application):

    """Command line application for interacting with InstaCli."""

    commands = [
        (cli_commands.Spiders, "commands")
    ]

    def setup(self):
        """Setup the command line parser.

        Extend the parser configuration in order to expose all
        the received commands.
        """
        self._parser = argparse.ArgumentParser()
        commands = self._parser.add_subparsers(title="[commands]",
                                               dest="command")

        self._register_parser("commands", commands)


def main():
    """The Cars Scrap command line application."""
    logging.setup(CONFIG, "arias")
    arias = AriasCli(sys.argv[1:])
    arias.run()
    return arias.result

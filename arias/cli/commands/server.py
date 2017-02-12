import os
import signal

import cherrypy
from oslo_log import log as logging

from arias import api as arias_api
from arias.cli import base as cli_base
from arias.common import constant
from arias.common import exception


LOG = logging.getLogger(__name__)


class Start(cli_base.Command):

    """Start the Arias API."""

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser("start",
                                         help="Start the Arias API.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """Start the Arias API."""
        pid = os.getpid()
        with open(constant.PID_TMP_FILE, "w") as file_handle:
            file_handle.write(str(pid))
        cherrypy.quickstart(arias_api.Root(), "/", arias_api.Root.config())


class Stop(cli_base.Command):

    """Stop the Arias API."""

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser("stop", help="Stop the Arias API.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """Stop the Arias API."""
        pid = None
        try:
            with open(constant.PID_TMP_FILE, "r") as file_handle:
                pid = int(file_handle.read().strip())
        except (ValueError, OSError) as exc:
            LOG.error("Failed to get server PID: %s", exc)
            raise exception.NotFound("Failed to get server PID.")

        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as exc:
            LOG.error("Failed to shutdown the server: %s", exc)
            return False

        return True


class Server(cli_base.Group):

    """Group for all the available server actions."""

    commands = [(Start, "actions"), (Stop, "actions")]

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "server",
            help="Operations related to the Arias API (start/stop).")

        actions = parser.add_subparsers()
        self._register_parser("actions", actions)

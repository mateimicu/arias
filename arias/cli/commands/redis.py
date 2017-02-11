"""
Redis CLI.
"""

from __future__ import print_function
import collections
import json

from oslo_log import log as logging
import prettytable

from arias.cli import base as cli_base
from arias.common import redisdb
from arias.common import constant
from arias.common import util

LOG = logging.getLogger(__name__)


class _ListNamespaces(cli_base.Command):

    """List the namespaces."""

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "list", help="List the available namespaces.")
        parser.add_argument(
            "--match", dest="match", default="*", 
            help="Regex expresion to match the namespace.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """Get all the namespaces."""
        redis_con = redisdb.RedisConnection()
        match = constant.NAMESPACE_FORMAT.format(self.args.match)

        namespaces = list(redis_con.rcon.scan_iter(match=match))

        # eliminte the prefix
        namespaces = [namespace.split(constant.NAMESPACE_FORMAT.format(""), 1)[-1] for
                        namespace in namespaces]
        return namespaces

    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        table = prettytable.PrettyTable(["NameSpace"])
        for namespace in result:
            table.add_row([namespace])
        print(table)


class _ShowNamespaces(cli_base.Command):

    """Show the items from a namespace."""

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "show", help="Show the items from a namespace")
        parser.add_argument(
            "--namespace", dest="namespace", required=True, 
            help="The name of the namespace.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """Show the namespace."""
        con = redisdb.RedisConnection()

        namespace = constant.NAMESPACE_FORMAT.format(self.args.namespace)
        raw_items = con.rcon.hgetall(namespace)

        # The case when there are no items in this namespace
        if not raw_items:
            return None

        cooked_items = {}
        for key, item in raw_items.items():
            cooked_item = json.loads(item)
            cooked_items[key] = cooked_item

        # Use the last item to get the keys
        keys = json.loads(raw_items.popitem()[1]).keys()
        return cooked_items, keys

    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        if not result:
            print(util.empty_table())
        else:
            items, keys = result
            table = prettytable.PrettyTable(keys.insert(0, "Key"))
            for key, item in items.items():
                row = [key]
                for key in keys:
                    row.append(item.get(key, ""))
                table.add_row(row)
            print(table)


class Redis(cli_base.Group):

    """Group for all the available namespace actions."""

    commands = [
        (_ListNamespaces, "actions"),
        (_ShowNamespaces, "actions"),
    ]

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "redis", help="Operations related to namespace management.")

        actions = parser.add_subparsers()
        self._register_parser("actions", actions)

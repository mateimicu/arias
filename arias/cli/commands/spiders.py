"""
Spiders CLI.
"""

from __future__ import print_function
import collections

from oslo_log import log as logging
import prettytable

from arias.cli import base as cli_base
from arias.common import util
from arias.spiders import factory as spider_factory

LOG = logging.getLogger(__name__)

SpiderInfo = collections.namedtuple("SpiderInfo",
                                    "name websites description start_urls")


class _ListSpiders(cli_base.Command):

    """List the spiders."""

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "list", help="List the availible tasks.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """List the spiders."""
        raw_spiders = spider_factory.SpiderFactory.get_items()
        spiders = []
        for spider in raw_spiders:
            cooked_spider = SpiderInfo(
                name=spider.name,
                websites=util.join_with_space(spider.allowed_domains),
                description=spider.__doc__ if spider.__doc__ else "",
                start_urls=util.join_with_space(spider.start_urls))

            spiders.append(cooked_spider)
        return spiders

    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        table = prettytable.PrettyTable(
            ["Name", "Websites", "Description", "Start Urls"])
        for spider in result:
            table.add_row([spider.name,
                           spider.websites,
                           spider.description,
                           spider.start_urls])
        print(table)


class Spiders(cli_base.Group):

    """Group for all the available spider actions."""

    commands = [
        (_ListSpiders, "actions")
    ]

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "spider", help="Operations related to spider management.")

        actions = parser.add_subparsers()
        self._register_parser("actions", actions)

"""
Crawl CLI.
"""

from __future__ import print_function

from oslo_log import log as logging

from arias.cli import base as cli_base
from arias.tasks import factory as task_factory

LOG = logging.getLogger(__name__)


class _StartCrawler(cli_base.Command):

    """Start a crawling."""

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "start", help="Start crawling.")
        parser.add_argument(
            "--spider", dest="spider", required=True,
            help="The spider you want to use.")
        parser.add_argument(
            "--pipeline", dest="pipeline", required=True,
            help="The pipelane you want to use.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """Start the crawling."""
        task = task_factory.get_task(
            spider_name=self.args.spider,
            pipeline_name=self.args.pipeline)

        return task.run()

    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        LOG.info("Crawling done!")

    def _on_task_fail(self, exc):
        """What to do if the crawling fails."""
        LOG.error("Crawling failed with message %(msg)s" % exc)


class Crawl(cli_base.Group):

    """Group for all the available crawling actions."""

    commands = [
        (_StartCrawler, "actions")
    ]

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "crawl", help="Operations related to crawl management.")

        actions = parser.add_subparsers()
        self._register_parser("actions", actions)

"""
Pipeline CLI.
"""

from __future__ import print_function
import collections

from oslo_log import log as logging
import prettytable

from arias.cli import base as cli_base
from arias.pipelines import factory as pipelines_factory

LOG = logging.getLogger(__name__)

PipelineInfo = collections.namedtuple("PipelineInfo", "name, description")


class _ListPipeline(cli_base.Command):

    """List the pipelines."""

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "list", help="List the availible pipelines.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """List the pipelines."""
        raw_pipeline = pipelines_factory.PipelineFactory.get_items()
        pipelines = []
        for pipeline in raw_pipeline:
            cooked_pipeline = PipelineInfo(
                name=pipeline.__name__,
                description=pipeline.__doc__ if pipeline.__doc__ else "")
            pipelines.append(cooked_pipeline)
        return pipelines

    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        table = prettytable.PrettyTable(["Name", "Description"])
        for pipeline in result:
            table.add_row([pipeline.name, pipeline.description])
        print(table)


class Pipelines(cli_base.Group):

    """Group for all the available pipelines actions."""

    commands = [
        (_ListPipeline, "actions")
    ]

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "pipeline", help="Operations related to pipeline management.")

        actions = parser.add_subparsers()
        self._register_parser("actions", actions)

"""Base class for workers."""

import abc

from oslo_log import log as logging
from scrapy import crawler
from scrapy import settings 

from arias.common import redisdb
from arias.tasks import base
from arias.common import exception
from arias import config as arias_config

CONFIG = arias_config.CONFIG
LOG = logging.getLogger(__name__)

import json

class AriasTasks(base.BaseTask):
    """Structure of a Task."""

    def __init__(self):
        super(AriasTasks, self).__init__()
        self._name = self.__class__.__name__

        self._spider = spider
        self._pipeline = pipeline

        pipeline_path = "{}.{}".format(pipeline.__module__,
                                       pipeline.__name__)
        self._settings = settings.Settings()
        self._settings.set('ITEM_PIPELINES', {pipeline_path: 100})

        self._crawler_process = crawler.CrawlerProcess(
            settings=self._settings)

    def _on_task_done(self, result):
        """Store each item """
        LOG.info("Task done {name}".format(
                 name=self.name))

    def _on_task_fail(self, exc):
        """Log the error and set the status."""
        LOG.error("Task failed {name} with error {error}".format(
                  name=self.name, error=exc))

    def prologue(self):
        """Executed once before the command starts."""
        # TODO(mmicu): set the status to "Doing"
        super(AriasTasks, self).prologue()

        # Add the spider to the crawler process
        self._crawler_process.crawl(self._spider)

    @abc.abstractmethod
    def _work(self):
        """Start the crawling process."""
        LOG.info("Started crawling {}".format(self._name))
        self._crawler_process.start(stop_after_crawl=True)

    def epilogue(self):
        """Executed once after the is done.."""
        # TODO(mmicu): set the status to "Done"

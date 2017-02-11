"""Base spider."""

import abc

import scrapy
import six


@six.add_metaclass(abc.ABCMeta)
class BaseSpider(scrapy.Spider):
    """Base class for all the spiders."""

    @abc.abstractmethod
    def parse(self, response):
        """Parse the response."""

"""
Base class for Pipelines
"""
import abc

import six

KEY_FORMAT = "{name}/{id}"


@six.add_metaclass(abc.ABCMeta)
class BasePipeline(object):
    """Base class for All the pipelines."""

    def get_key(self, item, spider):
        """Key format for every item."""
        return KEY_FORMAT.format(name=spider.name,
                                 id=item.get("id", ""))

    @abc.abstractmethod
    def process_item(self, item, spider):
        """How to process every item."""

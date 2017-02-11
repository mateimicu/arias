"""
Base class for Pipelines
"""
import abc
import uuid

from arias.common import constant

import six


@six.add_metaclass(abc.ABCMeta)
class BasePipeline(object):
    """Base class for All the pipelines."""

    def get_key(self, item, spider):
        """Key format for every item."""
        """Key format for every item.
        
        :param item: The item we want to store
        :param spider: The spider that fetched the item
        """
        return constant.KEY_FORMAT.format(name=spider.name, 
                id=item.get("id", str(uuid.uuid4())))

    def get_namespace(self, spider):
        """Namespace format for every spider.

        :param spider: The spider that fetche the item
        """
        return constant.NAMESPACE_FORMAT.format(spider.name)

    @abc.abstractmethod
    def process_item(self, item, spider):
        """How to process every item."""

"""A collection of utilities used across the project."""

import importlib

from arias.common import exception


def get_attribute(root, attribute):
    """Search for the received attribute name in the object tree.

    :param root: the root object
    :param attribute: the name of the required attribute
    """
    command_tree = [root]
    while command_tree:
        current_object = command_tree.pop()
        if hasattr(current_object, attribute):
            return getattr(current_object, attribute)

        parent = getattr(current_object, "parent", None)
        if parent:
            command_tree.append(parent)

    raise exception.AriasException("The %(attribute)r attribute is "
                                   "missing from the object tree.",
                                   attribute=attribute)


def join_with_space(items):
    """Join with `, ` the items.

    :param items: The items we want to join
    """
    return ", ".join([str(item) for item in items])


class BaseFactory(object):
    """Base class for all Factories."""

    # The base class for all the items
    BASE_CLASS = None

    # The prefix patch for all the items
    PREFIX = ""

    # A list with all the items
    ITEMS = []

    # The name of the factory
    NAME = ""

    @classmethod
    def get_items(cls):
        """Return a list with all the items."""
        all_items = []
        for item_module in cls.ITEMS:
            module_name = "{}.{}".format(cls.PREFIX, item_module)
            module = importlib.import_module(module_name)
            for item in dir(module):
                item = getattr(module, item)
                try:
                    if (not issubclass(item, cls.BASE_CLASS) or
                            item == cls.BASE_CLASS):
                        continue
                except (exception.AriasException, TypeError):
                    continue
                all_items.append(item)

        return all_items

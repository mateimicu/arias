#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Factory to get all the spiders.
"""

from arias.common import util
from arias.spiders import base


class SpiderFactory(util.BaseFactory):
    """Factory to get all the spiders."""

    # The base class for all the items
    BASE_CLASS = base.BaseSpider

    # The prefix patch for all the items
    PREFIX = "arias.spiders"

    # A list with all the items
    ITEMS = [
        "dmoz",
    ]

    # The name of the factory
    NAME = "spider_factory"

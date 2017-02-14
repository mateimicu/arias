"""
Spider utils.
"""

import collections

from arias.spiders import factory as spider_factory
from arias.common import util

SpiderInfo = collections.namedtuple("SpiderInfo",
                                    "name websites description start_urls")


def get_spiders_info():
    """Get a list with all the spiders."""
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

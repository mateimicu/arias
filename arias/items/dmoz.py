"""Test Item class."""

import scrapy


class DmozItem(scrapy.Item):
    """Dmoz test item."""
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

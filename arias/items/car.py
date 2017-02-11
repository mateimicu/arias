"""Item class for a car."""

import scrapy


class Car(scrapy.Item):
    """Car item."""
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    number = scrapy.Field()

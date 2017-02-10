"""Item loader for each Car Objects."""

from scrapy import loader
from scrapy.loader import processors

class CarLoader(loader.ItemLoader):
    default_output_processor = processors.Join()
    default_input_processor = processors.MapCompose(unicode.strip)



"""Item loader for Dmoz test Item."""

from scrapy import loader
from scrapy.loader import processors


class DmozItemLoader(loader.ItemLoader):
    """Dmoz test loader."""
    default_input_processor = processors.MapCompose(unicode.strip)
    default_output_processor = processors.TakeFirst()

    desc_out = processors.Join()

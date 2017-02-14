"""Item loader for each Car Objects."""

from arias.common import util

from scrapy import loader
from scrapy.loader import processors


class CarLoader(loader.ItemLoader):
    """Loader for the Car object."""
    # TODO(mmicu): make loaders more general,
    # maybe add them as a config option when
    # running a task
    default_output_processor = processors.Join()
    default_input_processor = processors.MapCompose(
        util.get_unicode_string_type().strip)

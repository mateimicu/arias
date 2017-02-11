"""Dmoz test pipelate to save an Item."""

import json

from arias.pipelines import base


class JsonWriterPipeline(base.BasePipeline):
    """Json Pipeline."""

    # The output filename
    file_name = "item.json"

    def __init__(self):
        """Open the file."""
        self.file = open(self.file_name, 'wb')

    def process_item(self, item, spider):
        """Parse the item."""
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

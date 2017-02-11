"""Dmoz test pipelate to save an Item."""

from arias.pipelines import base

import json


class JsonWriterPipeline(base.BasePipeline):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

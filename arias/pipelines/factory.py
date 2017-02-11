"""Factory for all the pipelines."""

from arias.common import util
from arias.pipelines import base


class PipelineFactory(util.BaseFactory):
    """Facoty for All pipeline classes."""

    # The base class for all the items
    BASE_CLASS = base.BasePipeline

    # The prefix patch for all the items
    PREFIX = "arias.pipelines"

    # A list with all the items
    ITEMS = [
        "dmoz_pipeline",
        "redis_pipeline"
    ]

    # The name of the factory
    NAME = "pipeline_factory"

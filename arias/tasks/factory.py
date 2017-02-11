"""Factory for tasks."""

from arias.common import exception
from arias.pipelines import factory as pipeline_factory
from arias.spiders import factory as spider_factory
from arias.tasks import task


def get_task(spider_name, pipeline_name):
    """Get a new Task object.

    :param spider_name: The spider name you want to use.
    :param pipeline_name: The pipeline name you want to use
    """
    spider = None
    pipeline = None

    # Get the spider class
    for item in spider_factory.SpiderFactory.get_items():
        if item.name == spider_name:
            spider = item
            break

    # Get the pipeline class
    for item in pipeline_factory.PipelineFactory.get_items():
        if item.__name__ == pipeline_name:
            pipeline = item
            break

    if spider is None:
        raise exception.InvalidName(
            name=spider_name, list_name="spiders")

    if pipeline is None:
        raise exception.InvalidName(
            name=pipeline_name, list_name="pipelines")

    return task.AriasTasks(spider=spider, pipeline=pipeline)

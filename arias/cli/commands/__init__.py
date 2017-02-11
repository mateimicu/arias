"""
Commands for the project.
"""

from arias.cli.commands import crawl
from arias.cli.commands import pipelines
from arias.cli.commands import spiders
from arias.cli.commands import redis

Spiders = spiders.Spiders
Pipelines = pipelines.Pipelines
Crawl = crawl.Crawl
Redis = redis.Redis

"""
Commands for the project.
"""

from arias.cli.commands import crawl
from arias.cli.commands import pipelines
from arias.cli.commands import server
from arias.cli.commands import spiders
from arias.cli.commands import redis

Crawl = crawl.Crawl
Pipelines = pipelines.Pipelines
Server = server.Server
Spiders = spiders.Spiders
Redis = redis.Redis

"""Redis pipelate to save an Item."""

import json

from arias.common import redisdb
from arias.pipelines import base


class RedisPipeline(base.BasePipeline):
    """Redis pipeline.

    Save the items in a redis database.
    """

    def __init__(self):
        """Create a Redis Connection."""
        self._redis = redisdb.RedisConnection()

    def process_item(self, item, spider):
        """Process the item.

        Save the item in the redis db.
        """
        key = self.get_key(item, spider)
        self._redis.rcon.hset(spider.name, key,
                              json.dumps(dict(item)))

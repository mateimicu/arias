"""Redis pipelate to save an Item."""

import json

from arias.common import redisdb
from arias.pipelines import base


class RedisPipeline(base.BasePipeline):

    def __init__(self):
        self._redis = redisdb.RedisConnection()

    def process_item(self, item, spider):
        key = self.get_key(item, spider)
        self._redis.rcon.hset(spider.name, key, 
                              json.dumps(dict(item)))

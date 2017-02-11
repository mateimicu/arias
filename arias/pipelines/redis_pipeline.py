"""Redis pipelate to save an Item."""

import json

from scrapy.exceptions import DropItem

from arias.common import redisdb
from arias.items import car

class CarPipeline(object):

    def __init__(self):
        self._rc = redisdb.RedisConnection()


    def process_item(self, item, spider):
        self._redis.rcon.hset(self._spider.website, str(key), 
                              json.dumps(dict(item)))



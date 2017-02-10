"""Redis conection utils."""

from oslo_log import log as logging
import redis

from arias.common import exception
from arias import config as arias_config

CONFIG = arias_config.CONFIG
LOG = logging.getLogger(__name__)


class RedisConnection(object):

    """High level wrapper over the redis data structures operations."""

    def __init__(self):
        """Instantiates objects able to store and retrieve data."""
        self._rcon = None
        self._host = CONFIG.redis.host
        self._port = CONFIG.redis.port
        self._db = CONFIG.redis.database
        self.refresh()

    def _connect(self):
        """Try establishing a connection until succeeds."""
        try:
            rcon = redis.StrictRedis(self._host, self._port, self._db)
            # Return the connection only if is valid and reachable
            if not rcon.ping():
                return None
        except (redis.ConnectionError, redis.RedisError) as exc:
            LOG.error("Failed to connect to Redis Server: %s", exc)
            return None

        return rcon

    def refresh(self, tries=3):
        """Re-establish the connection only if is dropped."""
        for _ in range(tries):
            try:
                if not self._rcon or not self._rcon.ping():
                    self._rcon = self._connect()
                else:
                    break
            except redis.ConnectionError as exc:
                LOG.error("Failed to connect to Redis Server: %s", exc)
        else:
            raise exception.AriasException(
                "Failed to connect to Redis Server.")

        return True

    @property
    def rcon(self):
        """Return a Redis connection."""
        self.refresh()
        return self._rcon

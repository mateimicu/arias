"""REST-like API base-class.

(Beginning of) the contract that all the resources must follow.
"""
import cherrypy

from oslo_log import log as logging

from arias import config as arias_config
from arias.common import redisdb

CONFIG = arias_config.CONFIG
LOG = logging.getLogger(__name__)


class BaseAPI(object):

    """Contract class for all API endpoints."""

    _cp_config = {'tools.staticdir.on': False}

    exposed = True
    """Whether this application should be available for clients."""

    resources = None
    """A list that contains all the resources (endpoints) available for the
    current metadata service."""

    def __init__(self, parent=None):
        self._parent = parent

        for raw_resource in self.resources or []:
            try:
                alias, resource = raw_resource
                setattr(self, alias, resource(self))
            except ValueError:
                LOG.error("Invalid resource %r provided.", raw_resource)

    @property
    def parent(self):
        """Return the object that contains the current resource."""
        return self._parent

    def GET(self):
        """ArestorV1 resource representation."""
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return "\n".join([endpoint for endpoint, _ in self.resources or []])


class Resource(object):

    """Contract class for all resources."""

    def __init__(self, parent):
        """Initialize a new Resource."""
        self._parent = parent
        self._redis = redisdb.RedisConnection()

    @property
    def parent(self):
        """Return the object that contains the current resource."""
        return self._parent

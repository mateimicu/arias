"""Arias API endpoint for spider management."""

import cherrypy
from oslo_log import log as logging

from arias.api import base as base_api
from arias.spiders import util as spiders_util


LOG = logging.getLogger(__name__)

class ListSpiders(base_api.Resource):

    exposed = True

    """List All spiders."""

    @cherrypy.tools.json_out()
    def GET(self, match="*"):
        """List the spiders."""
        connection = self._redis.rcon
        spiders = spiders_util.get_spiders_info()

        response = {"spiders": [spider._asdict() for spider in spiders]}
        LOG.info(response)
        return response

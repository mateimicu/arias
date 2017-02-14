"""Arias API endpoint for spider management."""

import cherrypy
from oslo_log import log as logging

from arias.api import base as base_api
from arias.spiders import util as spiders_util


LOG = logging.getLogger(__name__)


class ListSpiders(base_api.Resource):
    """List All spiders."""

    exposed = True

    @staticmethod
    @cherrypy.tools.json_out()
    def GET():
        """List the spiders."""
        spiders = spiders_util.get_spiders_info()

        response = {"spiders": [spider._asdict() for spider in spiders]}
        LOG.info(response)
        return response

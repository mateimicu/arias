"""The module contains the / endpoint object for Arias API."""

import os

import cherrypy

from arias.api import base as api_base
from arias.api import spiders
from arias import config as arias_config

CONFIG = arias_config.CONFIG


class Root(api_base.BaseAPI):

    """The / endpoint for the Arias API."""

    resources = [
        ("spider", spiders.SpiderEndpoint),
    ]

    @classmethod
    def config(cls):
        """Prepare the configurations."""
        return {
            'global': {
                'server.socket_host': CONFIG.api.host,
                'server.socket_port': CONFIG.api.port,
                'environment': CONFIG.api.environment,
                'log.screen': True,
                'log.error_file': os.path.join(CONFIG.log_dir or "",
                                               "arias-api-error.log"),
                'server.thread_pool': CONFIG.api.thread_pool,
            },
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }

    # TODO(mmicu): The GET endpoint will serve the home webpage and the rest will be the api

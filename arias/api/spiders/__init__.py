"""Spiders endpoint for the Arias project."""

from arias.api import base as base_api
from arias.api.spiders import resource


class SpiderEndpoint(base_api.BaseAPI):

    """Spider endpoint for the Arias API."""

    # A list that contains all the resources (endpoints) available for the
    # current metadata service
    resources = [
        ("list", resource.ListSpiders),
    ]

    exposed = True
    # Whether this application should be available for clients

"""Config options available for the arias setup."""

from oslo_config import cfg

from arias.config import base as conf_base


class AriasOptions(conf_base.Options):

    """Config options available for the arias setup."""

    def __init__(self, config):
        super(AriasOptions, self).__init__(config, group="DEFAULT")
        self._options = [
            cfg.StrOpt(
                "resources", default="", required=True,
                help="An url that holds the resources usually from "
                     "/argus/resources available on the web."),
        ]

    def register(self):
        """Register the current options to the global ConfigOpts object."""
        group = cfg.OptGroup(self.group_name, title='Arias Options')
        self._config.register_group(group)
        self._config.register_opts(self._options, group=group)

    def list(self):
        """Return a list which contains all the available options."""
        return self._options

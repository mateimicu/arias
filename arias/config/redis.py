"""Config options available for the redis database."""

from oslo_config import cfg

from arias.config import base as conf_base


class RedisOptions(conf_base.Options):

    """Config options available for the arias setup."""

    def __init__(self, config):
        super(RedisOptions, self).__init__(config, group="redis")
        self._options = [
            cfg.StrOpt(
                "host", default="127.0.0.1",
                help="The IP address or the host name of the server."),
            cfg.IntOpt(
                "port", default=6379, required=True,
                help="The port that should be used by the current "
                     "metadata service."),
            cfg.IntOpt(
                "database", default=0, required=True,
                help="The name of the database that should be used."),
        ]

    def register(self):
        """Register the current options to the global ConfigOpts object."""
        group = cfg.OptGroup(self.group_name, title='Redis Options')
        self._config.register_group(group)
        self._config.register_opts(self._options, group=group)

    def list(self):
        """Return a list which contains all the available options."""
        return self._options

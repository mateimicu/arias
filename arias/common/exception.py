"""Arias base exception handling."""


class AriasException(Exception):
    """Base Arias exception

    To correctly use this class, inherit from it and define
    a `template` property.

    That `template` will be formated using the keyword arguments
    provided to the constructor.
    """

    template = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        message = message or self.template

        try:
            message = message % kwargs
        except (TypeError, KeyError):
            # Something went wrong during message formatting.
            # Probably kwargs doesn't match a variable in the message.
            message = ("Message: %(template)s. Extra or "
                       "missing info: %(kwargs)s" %
                       {"template": message, "kwargs": kwargs})

        super(AriasException, self).__init__(message)


class CliError(AriasException):

    """Something went wrong during the processing of command line."""

    template = "Something went wrong during the procesing of command line."


class Invalid(AriasException):

    """The received object is not valid."""

    template = "Unacceptable parameters."


class NotFound(AriasException):

    """The required object is not available in container."""

    template = "The %(object)r was not found in %(container)s."


class NotSupported(AriasException):

    """The functionality required is not available in the current context."""

    template = "%(feature)s is not available in %(context)s."


class InvalidName(AriasException):

    """The name was not found in the context."""

    template = "%(name)s not found in the %(list_name) list."

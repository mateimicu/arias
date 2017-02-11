"""Base class for workers."""

import abc

from arias.common import exception

import six


@six.add_metaclass(abc.ABCMeta)
class BaseTask(object):
    # NOTE(mmicu): We might use celery for this tasks in the future
    # keep this class as clean a posible

    """Contract class for all the Tasks."""

    def __init__(self):
        self._name = self.__class__.__name__

    @property
    def name(self):
        """The name of the current task."""
        return self._name

    @abc.abstractmethod
    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        pass

    @abc.abstractmethod
    def _on_task_fail(self, exc):
        """What to do when the program fails processing a task."""
        pass

    def prologue(self):
        """Executed once before the command starts."""
        pass

    @abc.abstractmethod
    def _work(self):
        """Override this with your desired procedures."""
        pass

    def epilogue(self):
        """Executed once after the is done.."""
        pass

    def run(self):
        """Run the worker."""
        result = None

        try:
            self.prologue()
            result = self._work()
            self.epilogue()
        except exception.AriasException as exc:
            self._on_task_fail(exc)
        else:
            self._on_task_done(result)

        return result

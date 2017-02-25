"""
Spiders CLI.
"""

from __future__ import print_function

import abc

import docker
import six

from oslo_log import log as logging
import prettytable

from arias.cli import base as cli_base
from arias.common import constant
from arias.spiders import util as spiders_util

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class _DokerCommand(cli_base.Command):

    """Base class for all the commands that are ussing docker."""

    def __init__(self, parent, parser):
        super(_DokerCommand, self).__init__(parent, parser)
        self._docker = None
        self._command_name = ""

    def _prologue(self):
        """Executed once before the command running."""
        super(_DokerCommand, self)._prologue()
        LOG.debug("Create the docker client.")
        self._docker = docker.DockerClient(
            base_url=constant.DOCKER_BASE_URL)

    @staticmethod
    def _get_full_name(image_name, tag="latest"):
        """Return the full name of a docker image.
        
        :param image_name: The image name.
        :param tag: The image tag.
        """
        return "{}:{}".format(image_name, tag)

    def _image_exists(self, image_name, tag="latest"):
        """Check if the image exists locally."""
        full_name = self._get_full_name(image_name, tag)
        for image in self._docker.images.list():
            if image.tags == full_name:
                return True

        return False

    def _cleaup(self):
        """Clean up an old container with the same name."""
        # TODO(mmicu): When we use a state for this app
        # allow a diferite name `--container-name 'redis-2'`
        # and cleanup the conflicting container only when 
        # `-f --force` is provided
        for container in self._docker.containers.list(all=True):
            if container.name == self._container_name:
                LOG.info("Stop and remove container: %s", container.short_id)
                container.stop(timeout=constant.DOCKER_STOP_TIMEOUT)
                container.remove(force=True)
                break

    def _pull_image(self, image, tag="latest"):
        """Download the image (if not exists) or updates for it."""
        full_name = self._get_full_name(image, tag)

        LOG.info("Pulling %s", full_name)
        try:
            self._docker.images.pull(full_name)
        except docker.errors.APIError as ex:
            LOG.info("Error pulling %s", ex)
            return False

        return True

class _DeployRedis(_DokerCommand):
    """Deploy Redis."""

    def __init__(self, parent, parser):
        """Initialize the object."""
        super(_DeployRedis, self).__init__(parent, parser)
        self._container_name = "arias-redis"

    def setup(self):
        """Extend the parser configuration in order to expose all
        the received commands.
        """
        parser = self._parser.add_parser(
            "redis",
            help="Install the Ascipic on the current machine.")
        parser.add_argument(
            "--docker-image", dest="image", type=str,
            default="redis")
        parser.add_argument(
            "--image_tag", dest="tag", type=str,
            default="latest")
        parser.add_argument(
            "--exposed_port", dest="port", type=int,
            default=6379)
        parser.add_argument(
            "--mem_limit", dest="mem_limit", type=str, default="512m",
            help="Maximum amount of memory container is allowed to consume.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """Start on the current machine."""
        if not self._image_exists(self.args.image, self.args.tag):
            LOG.debug("The image %s was not found.", self.args.image)

        if not self._pull_image(self.args.image, self.args.tag):
            raise exception.CliError("Failed to pull the image: %(image)s",
                                     image=self.args.image)

        self._cleaup()

        container = self._docker.containers.run(
            image="%s:%s" % (self.args.image, self.args.tag),
            ports={"6379/tcp": self.args.port}, name=self._container_name,
            detach=True)
        LOG.debug("Started the container(for redis): %s", container.id)

        return container.short_id

    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        print("Starting the container(for redis): %s" % result)


class _DeployAPI(_DokerCommand):
    """Deploy API."""

    def __init__(self, parent, parser):
        """Initialize the object."""
        super(_DeployAPI, self).__init__(parent, parser)
        self._container_name = "arias-api"
        self._command = (
            "apt-get update -y && "
            "apt-get upgrade -y && "
            "apt-get install -y git python-pip && "
            "pip install git+https://github.com/micumatei/arias && "
            "arias server start; echo {port}"
        )
            # TODO(mmicu): Allow for cli options 'like --port'
            # `--host`:
            # Default < Config < CLI
            # "sudo arias server start --host 0.0.0.0 --port {port}"

    def setup(self):
        """Extend the parser configuration in order to expose all
        the received commands.
        """
        parser = self._parser.add_parser(
            "api",
            help="Install the Ascipic on the current machine.")
        parser.add_argument(
            "--docker-image", dest="image", type=str,
            default="ubuntu")
        parser.add_argument(
            "--image_tag", dest="tag", type=str,
            default="14.04.4")
        parser.add_argument(
            "--exposed_port", dest="port", type=int,
            default=80)
        parser.add_argument(
            "--mem_limit", dest="mem_limit", type=str, default="512m",
            help="Maximum amount of memory container is allowed to consume.")
        parser.set_defaults(work=self.run)

    def _work(self):
        """Start on the current machine."""
        if not self._image_exists(self.args.image, self.args.tag):
            LOG.debug("The image %s was not found.", self.args.image)

        if not self._pull_image(self.args.image, self.args.tag):
            raise exception.CliError("Failed to pull the image: %(image)s",
                                     image=self.args.image)

        self._cleaup()

        container = self._docker.containers.run(
            image="%s:%s" % (self.args.image, self.args.tag),
            ports={"{}/tcp".format(self.args.port): self.args.port},
            name=self._container_name,
            command = self._command.format(port=self.args.port),
            detach=True)
        LOG.debug("Started the container(for api): %s", container.id)

        return container.short_id

    def _on_task_done(self, result):
        """What to execute after successfully finished processing a task."""
        print("Starting the container(for api): %s", result)


class Deploy(cli_base.Group):

    """Group for all the available deployment actions."""

    commands = [
        (_DeployRedis, "actions"),
        (_DeployAPI, "actions")
    ]

    def setup(self):
        """Extend the parser configuration in order to expose this command."""
        parser = self._parser.add_parser(
            "deploy", help="Operations related to deployment management.")

        actions = parser.add_subparsers()
        self._register_parser("actions", actions)

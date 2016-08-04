"""Handle all events."""

# TODO: metaclass, to run function after service handler and send
# TODO: @config("value") decorator

from logging import getLogger

from uuid import uuid4
from base64 import b32encode

from .commands import COMMANDS

from .api import CactusAPI


class Handler(object):
    """Handle all events."""

    def __init__(self):

        self.logger = getLogger(__name__)

        api = CactusAPI(None)  # FIXME: pass correct channel

        self.commands = {  # TODO: make configurable
            "cactus": "Ohai! I'm CactusBot. :cactus",
            "test": "Test confirmed. :cactus",
            "help": "Check out my documentation at cactusbot.readthedocs.org."
        }

        self.commands.update(
            dict((command.COMMAND, command(api)) for command in COMMANDS)
        )

    async def send(self, *args, **kwargs):
        """Send a response."""
        raise NotImplementedError

    async def on_message(self, message, user):
        """Handle message events."""

        message = message.strip()

        self.logger.info("[%s] %s", user, message)

        if message.startswith('!') and len(message) > 1:
            args = message.split()
            command = args.pop(0)[1:]

            if command in self.commands:
                response = self.commands[command]
                if callable(response):
                    try:
                        response = await response(
                            *args,
                            username=user,
                            channel=getattr(self, "channel", "%CHANNEL%")
                        )
                    except Exception:
                        code = b32encode(uuid4().bytes).decode()[:12]
                        self.logger.exception("Exception. Code: %s.", code)
                        return ("An error occured. Please send code {} to "
                                "CactusDev.").format(code)  # FIXME: dynamic
            else:
                response = "Command not found."

            return response

        # TODO: spam protection

    async def on_join(self, user):
        """Handle join events."""
        self.logger.info("- %s joined", user)
        return "Welcome, @{}!".format(user)

    async def on_leave(self, user):
        """Handle leave events."""
        self.logger.info("- %s left", user)
        return "Goodbye, @{}.".format(user)

    async def on_follow(self, user):
        """Handle follow events."""
        self.logger.info("- %s followed", user)
        return "Thanks for the follow, @{}!".format(user)

    async def on_subscribe(self, user):
        """Handle subscribe events."""
        self.logger.info("- %s subscribed", user)
        return "Thanks for the subscription, @{}!".format(user)

"""Interact with CactusAPI."""

from .services.api import API


class CactusAPI(API):
    """Interact with CactusAPI."""

    URL = "http://107.170.60.137/api/v1/"

    def __init__(self, channel, **kwargs):
        super().__init__(**kwargs)

        self.channel = channel

    # FIXME: match API
    async def add_command(self, name, response, *, permissions={},
                          added_by=None):
        """Add a command."""
        data = {
            "response": response,
            "addedBy": added_by
        }
        return await self.patch("/channel/{channel}/command/{command}".format(
            channel=self.channel, command=name), data=data)

    # FIXME" match API
    async def remove_command(self, name, *, removed_by=None):
        """Remove a command."""
        data = {
            "removedBy": removed_by
        }
        return await self.delete("/channel/{channel}/command/{command}".format(
            channel=self.channel, command=name), data=data)

    # FIXME: match API
    async def get_command(self, name=None):
        """Get a command."""
        if name is not None:
            return await self.get(
                "/channel/{channel}/command/{command}".format(
                    channel=self.channel, command=name))
        return await self.get(
            "/channel/{channel}/command".format(channel=self.channel))

    # TODO: implement
    async def add_quote(self, quote, *, added_by=None):
        """Add a quote."""
        return "In development."

    # TODO: implement
    async def remove_quote(self, quote_id):
        """Remove a quote."""
        return "In development."

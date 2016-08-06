"""Interact with CactusAPI."""

from .services.api import API


class CactusAPI(API):
    """Interact with CactusAPI."""

    URL = "http://localhost:8000/api/v1/"

    def __init__(self, channel, **kwargs):
        super().__init__(**kwargs)

        self.channel = channel

    async def add_command(self, name, response, *, permissions={},
                          added_by=None):
        """Add a command."""

        data = {
            "response": response,
        }

        return await self.patch("/user/{channel}/command/{command}".format(
            channel=self.channel, command=name), data=data)

    async def remove_command(self, name, *, removed_by=None):
        """Remove a command."""
        data = {
            "removedBy": removed_by
        }
        return await self.delete("/user/{channel}/command/{command}".format(
            channel=self.channel, command=name), data=data)

    async def get_command(self, name=None):
        """Get a command."""
        if name is not None:
            return await self.get(
                "/user/{channel}/command/{command}".format(
                    channel=self.channel, command=name))
        return await self.get(
            "/user/{channel}/command".format(channel=self.channel))

    async def add_quote(self, quote, *, added_by=None):
        """Add a quote."""
        return "In development."

    async def remove_quote(self, quote_id):
        """Remove a quote."""
        return "In development."

    async def get_friend(self, name=None):
        """Get a list of friends."""
        if name is None:
            return await self.get("/channel/{channel}/friend")

        return await self.get("/channel/{channel}/friend/{name}".format(
            channel=self.channel, name=name))

    async def add_friend(self, username):
        """Add a friend."""
        return await self.patch("/channel/{channel}/friend/{name}".format(
            channel=self.channel, name=username))

    async def remove_friend(self, username):
        """Remove a friend."""
        return await self.delete("/channel/{channel}/friend/{name}".format(
            channel=self.channel, name=username))

"""Interact with CactusAPI."""

import json

from .services.api import API


class CactusAPI(API):
    """Interact with CactusAPI."""

    URL = "https://cactus.exoz.one/api/v1/"

    def __init__(self, channel, **kwargs):
        super().__init__(**kwargs)

        self.channel = channel

    async def request(self, method, endpoints, **kwargs):
        """Send HTTP request to endpoint."""

        if "headers" in kwargs:
            kwargs["headers"]["Content-Type"] = "application/json"
        else:
            kwargs["headers"] = {"Content-Type": "application/json"}

        return await super().request(method, endpoints, **kwargs)

    async def get_command(self, name=None):
        """Get a command."""

        if name is not None:
            return await self.get(
                "/user/{channel}/command/{command}".format(
                    channel=self.channel, command=name))
        return await self.get("/user/{channel}/command".format(
            channel=self.channel))

    async def add_command(self, name, response, *, user_level=0):
        """Add a command."""

        data = {
            "response": response,
            "userLevel": user_level  # TODO
        }

        return await self.patch(
            "/user/{channel}/command/{command}".format(
                channel=self.channel, command=name),
            data=json.dumps(data)
        )

    async def remove_command(self, name):
        """Remove a command."""
        return await self.delete("/user/{channel}/command/{command}".format(
            channel=self.channel, command=name))

    async def get_quote(self, quote_id=None):
        """Get a quote."""

        if quote_id is not None:
            return await self.get("/user/{channel}/quote/{id}".format(
                channel=self.channel, id=quote_id))
        return await self.get("/user/{channel}/quote".format(
            channel=self.channel), params={"random": True})

    async def add_quote(self, quote):
        """Add a quote."""

        data = {"quote": quote}

        return await self.post(
            "/user/{channel}/quote".format(channel=self.channel),
            data=json.dumps(data)
        )

    async def edit_quote(self, quote_id, quote):
        """Edit a quote."""

        data = {"quote": quote}

        return await self.patch(
            "/user/{channel}/quote/{quote_id}".format(
                channel=self.channel, quote_id=quote_id),
            data=json.dumps(data)
        )

    async def remove_quote(self, quote_id):
        """Remove a quote."""
        return await self.delete("/user/{channel}/quote/{id}".format(
            channel=self.channel, id=quote_id))

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

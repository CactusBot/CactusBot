"""Interact with the Beam API."""

from ..api import API


class BeamAPI(API):
    """Interact with the Beam API."""

    URL = "https://beam.pro/api/v1/"

    async def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        data = {
            "username": username,
            "password": password,
            "code": code
        }
        return await self.post("/users/login", data=data)

    async def get_channel(self, channel, **params):
        """Get channel data by username or ID."""
        return await self.get(
            "/channels/{channel}".format(channel=channel), params=params)

    async def get_chat(self, chat):
        """Get required data for connecting to a chat server by channel ID."""
        return await self.get("/chats/{chat}".format(chat=chat))

    async def remove_message(self, chat, message):
        """Remove a message from chat by ID."""
        return await self.delete("/chats/{chat}/message/{message}".format(
            chat=chat, message=message))

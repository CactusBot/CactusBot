"""Handle data from Beam."""

from logging import getLogger

import asyncio
import re

from .. import Handler

from .api import BeamAPI
from .chat import BeamChat
from .liveloading import BeamLiveloading


class BeamHandler(Handler):
    """Handle data from Beam services."""

    def __init__(self, channel):
        super().__init__()

        self.logger = getLogger(__name__)

        self.api = BeamAPI()

        self._channel = channel
        self.channel = ""

        self.chat = None
        self.liveloading = None

        self.chat_events = {
            "ChatMessage": self.on_message,
            "UserJoin": self.on_join,
            "UserLeave": self.on_leave
        }

        self.liveloading_events = {
            "channel": {
                "followed": self.on_follow,
                "subscribed": self.on_subscribe
            }
        }

    async def run(self, *auth):
        """Connect to Beam chat and handle incoming packets."""
        channel = await self.api.get_channel(self._channel)
        self.channel = str(channel["id"])
        self.api.channel = self.channel  # HACK

        user = await self.api.login(*auth)
        chat = await self.api.get_chat(channel["id"])

        self.chat = BeamChat(channel["id"], *chat["endpoints"])
        await self.chat.connect(user["id"], chat["authkey"])
        asyncio.ensure_future(self.chat.read(self.handle_chat))

        self.liveloading = BeamLiveloading(
            channel["id"], channel["user"]["id"]
        )
        await self.liveloading.connect()
        asyncio.ensure_future(self.liveloading.read(self.handle_liveloading))

    async def handle_chat(self, packet):
        """Handle chat packets."""

        data = packet.get("data")
        if data is None:
            return

        event = packet.get("event")
        if event in self.chat_events:
            await self.chat_events[event](data)
        elif packet.get("id") == "auth":
            if data.get("authenticated") is True:
                await self.send("CactusBot activated. Enjoy! :cactus")
            else:
                self.logger.error("Chat authentication failure!")

    async def handle_liveloading(self, packet):
        """Handle liveloading packets."""

        data = packet.get("data")
        if not isinstance(data, list) or not isinstance(data[0], str):
            return

        event = re.match(self.liveloading.INTERFACE_EXPR, data[0])
        if event is None:
            return

        event = event.groups()
        if event[1] in self.liveloading_events.get(event[0], {}):
            await self.liveloading_events[event[0]][event[1]](data[1])

    async def send(self, *args, **kwargs):
        """Send a packet to Beam."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send(*args, **kwargs)

    async def on_message(self, data):
        """Handle chat message packets from chat."""

        parsed = ''.join([
            chunk["text"] for chunk in data["message"]["message"]
        ])

        response = await super().on_message(parsed, data["user_name"])
        if response is not None:
            await self.send(response)

    async def on_join(self, data):
        """Handle user join packets from chat."""
        await self.send(await super().on_join(data["username"]))

    async def on_leave(self, data):
        """Handle user leave packets from chat."""
        if data["username"] is not None:
            await self.send(await super().on_leave(data["username"]))

    async def on_follow(self, data):
        """Handle follow packets from liveloading."""
        if data["following"]:
            await self.send(await super().on_follow(data["user"]["username"]))

    async def on_subscribe(self, data):
        """Handle subscribe packets from liveloading."""
        await self.send(await super().on_subscribe(data["user"]["username"]))

"""Interact with Beam liveloading."""

from logging import getLogger

import re
import json

import asyncio

from .. import WebSocket


class BeamConstellation(WebSocket):
    """Interact with Beam liveloading."""

    URL = "wss://constellation.beam.pro"

    RESPONSE_EXPR = re.compile(r'^(\d+)(.+)?$')
    INTERFACE_EXPR = re.compile(r'^([a-z]+):\d+:([a-z]+)')

    def __init__(self, channel, user):
        super().__init__(self.URL)

        self.logger = getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        assert isinstance(user, int), "User ID must be an integer."
        self.user = user

    async def read(self, handle):
        """Read packets from the liveloading WebSocket."""

        packet = await self.parse(await self.receive())

        await super().read(handle)

    async def initialize(self, *interfaces):
        """Subscribe to liveloading interfaces."""

        if not interfaces:
            interfaces = [
                "channel:{channel}:update".format(channel=self.channel),
                "channel:{channel}:status".format(channel=self.channel),
                "channel:{channel}:followed".format(channel=self.channel),
                "channel:{channel}:subscribed".format(channel=self.channel),
                "user:{user}:followed".format(user=self.user),
                "user:{user}:subscribed".format(user=self.user),
                "user:{user}:achievement".format(user=self.user)
            ]

        packet = {
            "type": "method",
            "method": "livesubscribe",
            "params": {
                "events": interfaces
            },
            "id": 1
        }

        self.websocket.send_str(json.dumps(packet))

        print(await self.websocket.receive())
        self.logger.info("Successfully subscribed to liveloading interfaces.")

"""Interact with Beam liveloading."""

"""
The MIT License

Copyright (c) 2016 CactusDev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from logging import getLogger

import re
import json

import asyncio

from ... import WebSocket


class BeamLiveloading(WebSocket):
    """Interact with Beam liveloading."""

    URL = "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket"

    RESPONSE_EXPR = re.compile(r'^(\d+)(.+)?$')
    INTERFACE_EXPR = re.compile(r'^([a-z]+):\d+:([a-z]+)')

    def __init__(self, channel, user):
        super().__init__(self.URL)

        self.logger = getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        assert isinstance(user, int), "User ID must be an integer."
        self.user = user

    async def read(self):
        """Read packets from the liveloading WebSocket."""

        packet = await self.parse(await self.receive())

        asyncio.ensure_future(self.ping(packet["data"]["pingInterval"] / 1000))

        await super().read()

    async def initialize(self, *interfaces):
        """Subscribe to liveloading interfaces."""

        if not interfaces:
            # TODO: dict of interfaces with callbacks
            interfaces = (
                "channel:{channel}:update",
                "channel:{channel}:status",
                "channel:{channel}:followed",
                "channel:{channel}:subscribed",
                "user:{user}:followed",
                "user:{user}:subscribed",
                "user:{user}:achievement"
            )

        interfaces = tuple(
            interface.format(channel=self.channel, user=self.user)
            for interface in interfaces
        )

        packet = [
            "put",
            {
                "method": "put",
                "headers": {},
                "data": {
                    "slug": interfaces
                },
                "url": "/api/v1/live"
            }
        ]
        self.websocket.send_str('420' + json.dumps(packet))

        self.logger.info("Successfully subscribed to liveloading interfaces.")

    async def ping(self, interval):
        """Periodically ping the liveloading server to sustain connection."""

        while True:
            self.websocket.send_str('2')
            await asyncio.sleep(interval)

    async def parse(self, packet):
        """Parse a packet from liveloading."""

        match = re.match(self.RESPONSE_EXPR, packet)

        data = match.group(2)
        if data is not None:
            try:
                data = json.loads(data)
            except ValueError:
                self.logger.exception("Invalid JSON: %s.", data)

        return {
            "code": match.group(1),
            "data": data
        }

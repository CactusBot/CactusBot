"""Interact with Beam chat."""


from logging import getLogger

import json

import itertools

from ... import WebSocket


class BeamChat(WebSocket):
    """Interact with Beam chat."""

    def __init__(self, channel, *endpoints):
        super().__init__(*endpoints)

        self.logger = getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        self._packet_counter = itertools.count()

    async def send(self, *args, max_length=500, **kwargs):
        """Send a packet."""

        # TODO: block before auth

        packet = {
            "type": "method",
            "method": "msg",
            "arguments": args,
            "id": kwargs.get("id") or self._packet_id
        }

        packet.update(kwargs)

        if packet["method"] == "msg":
            for message in packet.copy()["arguments"]:
                for index in range(0, len(message), max_length):
                    packet["arguments"] = (message[index:index+max_length],)
                    await super().send(json.dumps(packet))
        else:
            await super().send(json.dumps(packet))

    async def initialize(self, *auth):
        """Send an authentication packet."""
        await self.send(self.channel, *auth, method="auth", id="auth")
        # TODO: block until authentication response

    async def parse(self, packet):
        """Parse a received packet."""

        try:
            packet = json.loads(packet)
        except (TypeError, ValueError):
            self.logger.warning("Invalid JSON: %s.", packet, exc_info=True)
            return None, None
        else:
            if packet.get("error") is not None:
                self.logger.error(packet)
            else:
                self.logger.debug(packet)

            if packet.get("type") == "event":
                return packet.get("event"), packet.get("data")
            else:
                return None, packet

    @property
    def _packet_id(self):
        return next(self._packet_counter)

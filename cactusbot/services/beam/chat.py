"""Interact with Beam chat."""

import json

import itertools

from .. import WebSocket


class BeamChat(WebSocket):
    """Interact with Beam chat."""

    def __init__(self, channel, *endpoints):
        super().__init__(*endpoints)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        self._packet_counter = itertools.count()

    async def send(self, *args, **kwargs):
        """Send a packet."""

        # FIXME: chat length limit

        packet = {
            "type": "method",
            "method": "msg",
            "arguments": args,
            "id": kwargs.get("id") or self._packet_id
        }

        packet.update(kwargs)

        await super().send(json.dumps(packet))

    async def initialize(self, *auth):
        """Send an authentication packet."""
        await self.send(self.channel, *auth, method="auth", id="auth")

    async def parse(self, packet):
        """Parse a chat packet."""

        try:
            packet = json.loads(packet)
        except (TypeError, ValueError):
            self.logger.exception("Invalid JSON: %s.", packet)
            return None
        else:
            if packet.get("error") is not None:
                self.logger.error(packet)
            else:
                self.logger.debug(packet)
            return packet

    @property
    def _packet_id(self):
        return next(self._packet_counter)

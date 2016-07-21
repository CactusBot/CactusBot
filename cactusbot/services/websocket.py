"""Interact with WebSockets safely."""

from logging import getLogger

import asyncio

import itertools

from aiohttp import ClientSession
from aiohttp.errors import DisconnectedError, HttpProcessingError, ClientError


class WebSocket(ClientSession):
    """Interact with WebSockets safely."""

    def __init__(self, *endpoints):
        super().__init__()

        self.logger = getLogger(__name__)

        assert len(endpoints), "An endpoint is required to connect."

        self.websocket = None

        self._endpoint_cycle = itertools.cycle(endpoints)

    async def connect(self, *args, base=2, maximum=60, **kwargs):
        """Connect to a WebSocket."""

        _backoff_count = itertools.count()
        self.logger.debug("Connecting...")

        while True:
            try:
                self.websocket = await self.ws_connect(self._endpoint)
            except (DisconnectedError, HttpProcessingError, ClientError):
                backoff = min(base**next(_backoff_count), maximum)
                self.logger.debug("Retrying in %s seconds...", backoff)
                await asyncio.sleep(backoff)
            else:
                await self.initialize(*args, **kwargs)
                self.logger.info("Connection established.")
                return self.websocket

    async def send(self, packet):
        """Send a packet to the WebSocket."""
        assert self.websocket is not None, "Must connect to send."
        self.logger.debug(packet)
        self.websocket.send_str(packet)

    async def receive(self):
        """Receive a packet from the WebSocket."""
        return (await self.websocket.receive()).data

    async def read(self, handle):
        """Read packets from the WebSocket."""

        assert self.websocket is not None, "Must connect to read."
        assert callable(handle), "Handler must be callable."

        while True:
            packet = await self.receive()
            if isinstance(packet, str):
                packet = await self.parse(packet)
                if packet is not None:
                    asyncio.ensure_future(handle(packet))
            else:
                self.logger.warning("Connection lost. Reconnecting.")
                await self.connect()

    async def initialize(self):
        """Run initialization procedure."""
        pass

    async def parse(self, packet):
        """Parse a packet from the WebSocket."""
        return packet

    @property
    def _endpoint(self):
        return next(self._endpoint_cycle)

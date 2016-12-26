"""Handle data from Beam."""

import logging

import discord

from ...packets import MessagePacket
from .parser import DiscordParser


class DiscordHandler(discord.Client):
    """Handle data from Discord."""

    def __init__(self, handlers):

        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.parser = DiscordParser
        self.handlers = handlers  # HACK, potentially

    async def on_message(self, message):
        await self.handle("message", message.channel,
                          self.parser.parse_message(message))

    async def on_message_edit(self, before, after):
        await self.handle("edit", after.channel,
                          self.parser.parse_edit(before, after))

    async def on_message_delete(self, message):
        await self.handle("remove", message.channel,
                          self.parser.parse_message(message))

    async def handle(self, event, channel, packet):
        """Handle a packet event."""

        for response in self.handlers.handle(event, packet):
            if isinstance(response, MessagePacket):
                packet = self.parser.synthesize(response)
                await self.send_message(channel, packet)

    async def run(self, *args, **kwargs):
        await self.start(*args, **kwargs)

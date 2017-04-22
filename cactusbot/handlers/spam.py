"""Handle incoming spam messages."""

import aiohttp

from ..handler import Handler
from ..packets import BanPacket, MessagePacket

BASE_URL = "https://beam.pro/api/v1/channels/{username}"


async def get_user_id(username):
    """Retrieve Beam user ID from username."""
    async with aiohttp.get(BASE_URL.format(username=username)) as response:
        if response.status == 404:
            return 0
        return (await response.json())["id"]


class SpamHandler(Handler):
    """Spam handler."""

    def __init__(self, api):
        super().__init__()

        self.api = api

        self.config = {
            "max_score": 16,
            "max_emoji": 6,
            "allow_urls": False
        }

    async def on_message(self, packet):
        """Handle message events."""

        if packet.role >= 4:
            return

        user_id = await get_user_id(packet.user)
        if (await self.api.trust.get(user_id)).status == 200:
            return

        exceeds_caps = self.check_caps(''.join(
            chunk.text for chunk in packet if
            chunk.type == "text"
        ))
        exceeds_emoji = self.check_emoji(packet)
        contains_urls = self.contains_urls(packet)

        if exceeds_caps:
            return (MessagePacket("Please do not spam capital letters.",
                                  target=packet.user),
                    BanPacket(packet.user, 1),
                    StopIteration)

        if exceeds_emoji:
            return (MessagePacket("Please do not spam emoji.",
                                  target=packet.user),
                    BanPacket(packet.user, 1),
                    StopIteration)

        if contains_urls:
            return (MessagePacket("Please do not post URLs.",
                                  target=packet.user),
                    BanPacket(packet.user, 5),
                    StopIteration)

        return None

    async def on_config(self, packet):
        """Handle config update events."""

        if packet.type == "spam":
            self.config["max_emoji"] = packet.kwargs["maxEmoji"]
            self.config["max_score"] = packet.kwargs["maxCapsScore"]
            self.config["allow_urls"] = packet.kwargs["allowUrls"]

    def check_caps(self, message):
        """Check for excessive capital characters in the message."""
        return sum(char.isupper() - char.islower() for
                   char in message) > self.config["max_score"]

    def check_emoji(self, packet):
        """Check for excessive emoji in the message."""
        return sum(chunk.type == "emoji" for
                   chunk in packet) > self.config["max_emoji"]

    def contains_urls(self, packet):
        """Check for URLs in the message."""
        return not self.config["allow_urls"] and any(
            chunk.type == "url" and not
                chunk.text.strip() == "d.va" for chunk in packet)

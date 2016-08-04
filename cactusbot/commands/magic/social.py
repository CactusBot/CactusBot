"""Get social data."""

import json

from . import Command

import aiohttp


class Social(Command):
    """Get social data."""

    COMMAND = "social"

    @Command.subcommand(hidden=True)
    async def get(self, *args: False, channel: "channel"):
        """Get a social service if it's provived, or give it all."""

        social_data = await (await aiohttp.get(
            "https://beam.pro/api/v1/channels/{}".format(channel)
        )).json()

        social_data = social_data["user"]["social"]

        if not args:
            return str(channel)
        else:
            return "FAKE POTATO"

    DEFAULT = get

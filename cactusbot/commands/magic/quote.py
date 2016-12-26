"""Manage quotes."""

from aiohttp import get

from . import Command
from ...packets import MessagePacket


@Command.command()
class Quote(Command):
    """Manage quotes."""

    COMMAND = "quote"

    @Command.command(hidden=True)
    async def default(self, quote_id: r'[1-9]\d*'=None):
        """Get a quote based on ID. If no ID is provided, pick a random one."""

        if quote_id is None:
            response = await self.api.get_quote()
            if response.status == 404:
                return "No quotes have been added!"
            return (await response.json())["data"][0]["attributes"]["quote"]
        else:
            response = await self.api.get_quote(quote_id)
            if response.status == 404:
                return "Quote {} does not exist!".format(quote_id)
            return (await response.json())["data"]["attributes"]["quote"]

    @Command.command()
    async def add(self, *quote):
        """Add a quote."""
        response = await self.api.add_quote(' '.join(quote))
        data = await response.json()
        return "Added quote with ID {}.".format(
            data["data"]["attributes"]["quoteId"])

    @Command.command()
    async def edit(self, quote_id: r'[1-9]\d*', *quote):
        """Edit a quote based on ID."""
        response = await self.api.edit_quote(quote_id, ' '.join(quote))
        if response.status == 201:
            return "Added quote with ID {}.".format(quote_id)
        return "Edited quote with ID {}.".format(quote_id)

    @Command.command()
    async def remove(self, quote_id: r'[1-9]\d*'):
        """Remove a quote."""
        response = await self.api.remove_quote(quote_id)
        if response.status == 404:
            return "Quote {} does not exist!".format(quote_id)
        return "Removed quote with ID {}.".format(quote_id)

    @Command.command(hidden=True)
    async def inspirational(self):
        """Retrieve an inspirational quote."""
        try:
            data = await (await get(
                "http://api.forismatic.com/api/1.0/",
                params=dict(method="getQuote", lang="en", format="json")
            )).json()
        except Exception:
            return MessagePacket(
                "Unable to get an inspirational quote. Have a ",
                ("emoji", "🐹", "🐹"),
                " instead."
            )
        else:
            return "\"{quote}\" -{author}".format(
                quote=data["quoteText"].strip(),
                author=data["quoteAuthor"].strip() or "Unknown"
            )

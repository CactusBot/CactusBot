"""Manage quotes."""

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

from aiohttp import get

from . import Command


class Quote(Command):
    """Manage quotes."""

    COMMAND = "quote"

    @Command.subcommand(hidden=True)
    async def get(self, quote_id: r'[1-9]\d*'=None):
        """Get a quote based on ID. If no ID is provided, pick a random one."""
        if quote_id is None:
            return self.api.get_quote()
        return self.api.get_quote(quote_id)

    @Command.subcommand
    async def add(self, *quote, added_by: "username"):
        """Add a quote."""
        response = await self.api.add_quote(' '.join(quote), added_by=added_by)
        return "Added quote with ID {}.".format(response["data"]["id"])

    @Command.subcommand
    async def remove(self, quote_id: r'[1-9]\d*'):
        """Remove a quote."""
        try:
            self.api.remove_quote(quote_id)
        except Exception:  # FIXME: data, not exceptions
            return "Quote {} does not exist!".format(quote_id)
        else:
            return "Removed quote with ID {}.".format(quote_id)

    @Command.subcommand  # FIXME: make secret
    async def inspirational(self):
        """Retrieve an inspirational quote."""
        try:
            data = await (await get(
                "http://api.forismatic.com/api/1.0/",
                params=dict(method="getQuote", lang="en", format="json")
            )).json()
        except Exception:
            return ("Unable to get an inspirational quote. "
                    "Have a :hamster instead.")
        else:
            return "\"{quote}\" -{author}".format(
                quote=data["quoteText"].strip(),
                author=data["quoteAuthor"].strip() or "Unknown"
            )

    DEFAULT = get

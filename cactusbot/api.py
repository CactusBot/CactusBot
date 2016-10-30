"""Interact with CactusAPI."""

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

from .services.api import API


class CactusAPI(API):
    """Interact with CactusAPI."""

    URL = "http://107.170.60.137/api/v1/"

    def __init__(self, channel, **kwargs):
        super().__init__(**kwargs)

        self.channel = channel

    # FIXME: match API
    async def add_command(self, name, response, *, permissions={},
                          added_by=None):
        """Add a command."""
        data = {
            "response": response,
            "addedBy": added_by
        }
        return await self.patch("/channel/{channel}/command/{command}".format(
            channel=self.channel, command=name), data=data)

    # FIXME" match API
    async def remove_command(self, name, *, removed_by=None):
        """Remove a command."""
        data = {
            "removedBy": removed_by
        }
        return await self.delete("/channel/{channel}/command/{command}".format(
            channel=self.channel, command=name), data=data)

    # FIXME: match API
    async def get_command(self, name=None):
        """Get a command."""
        if name is not None:
            return await self.get(
                "/channel/{channel}/command/{command}".format(
                    channel=self.channel, command=name))
        return await self.get(
            "/channel/{channel}/command".format(channel=self.channel))

    # TODO: implement
    async def add_quote(self, quote, *, added_by=None):
        """Add a quote."""
        return "In development."

    # TODO: implement
    async def remove_quote(self, quote_id):
        """Remove a quote."""
        return "In development."

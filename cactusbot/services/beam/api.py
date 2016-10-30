"""Interact with the Beam API."""

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

from ..api import API


class BeamAPI(API):
    """Interact with the Beam API."""

    URL = "https://beam.pro/api/v1/"

    async def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        data = {
            "username": username,
            "password": password,
            "code": code
        }
        return await self.post("/users/login", data=data)

    async def get_channel(self, channel, **params):
        """Get channel data by username or ID."""
        return await self.get(
            "/channels/{channel}".format(channel=channel), params=params)

    async def get_chat(self, chat):
        """Get required data for connecting to a chat server by channel ID."""
        return await self.get("/chats/{chat}".format(chat=chat))

    async def remove_message(self, chat, message):
        """Remove a message from chat by ID."""
        return await self.delete("/chats/{chat}/message/{message}".format(
            chat=chat, message=message))

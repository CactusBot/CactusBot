"""Test the command command."""

import pytest

from cactusbot.commands.magic import Meta
from cactusbot.packets import MessagePacket

class MockAPI:
    """Fake API."""

    async def get_command(self, command=None):
        """Get commands."""

        class Response:
            """API response."""

            @property
            def status(self):
                """Status of the response."""
                return 200

            async def json(self):
                """JSON response."""

                if command:
                    return {
                        "data": {
                            "attributes": {
                                "count": 0,
                                "enabled": True,
                                "name": "testing",
                                "response": {
                                    "action": False,
                                    "message": [
                                        {
                                            "data": "testing!",
                                            "text": "testing!",
                                            "type": "text"
                                        },
                                        {
                                            "data": ":smile:",
                                            "text": ":)",
                                            "type": "emoji"
                                        }
                                    ],
                                    "target": None,
                                    "user": "Stanley"
                                },
                                "role": 0,
                                "token": "Stanley"
                            },
                            "id": "3f51fc4d-d012-41c0-b98e-ff6257394f75",
                            "type": "command"
                        },
                        "meta": {
                            "created": True
                        }
                    }
                else:
                    return {
                        "data": [
                            {
                                "attributes": {
                                    "count": 2,
                                    "enabled": True,
                                    "name": "testing",
                                    "response": {
                                        "action": False,
                                        "message": [
                                            {
                                                "data": "testing!",
                                                "text": "testing!",
                                                "type": "text"
                                            }
                                        ],
                                        "role": 1,
                                        "target": None,
                                        "user": "Stanley"
                                    },
                                    "token": "Stanley"
                                },
                                "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                                "type": "command"
                            },
                            {
                                "attributes": {
                                    "commandName": "testing",
                                    "count": 2,
                                    "enabled": True,
                                    "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                                    "name": "test",
                                    "response": {
                                        "action": False,
                                        "message": [
                                            {
                                                "data": "testing!",
                                                "text": "testing!",
                                                "type": "text"
                                            }
                                        ],
                                        "role": 1,
                                        "target": None,
                                        "user": "Stanley"
                                    },
                                    "token": "Stanley"
                                },
                                "id": "312ab175-fb52-4a7b-865d-4202176f9234",
                                "type": "aliases"
                            }
                        ]
                    }
        return Response()

    async def add_command(self, name, response, *, user_level=1):
        """Add a command."""

        class Response:
            """API response."""

            @property
            def status(self):
                """Status of the request."""
                return 200

            async def json(self):
                """JSON response."""

                return {
                    "data": {
                        "attributes": {
                            "count": 0,
                            "enabled": True,
                            "name": "testing",
                            "response": {
                                "action": False,
                                "message": [
                                    {
                                        "data": "lol!",
                                        "text": "lol!",
                                        "type": "text"
                                    },
                                    {
                                        "data": ":smile:",
                                        "text": ":)",
                                        "type": "emoji"
                                    }
                                ],
                                "role": 0,
                                "target": None,
                                "user": ""
                            },
                            "token": "innectic2"
                        },
                        "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                        "type": "command"
                    },
                    "meta": {
                        "edited": True
                    }
                }
        return Response()

    async def remove_command(self, name):
        """Remove a command."""

        class Response:
            """API response."""

            @property
            def status(self):
                """Status of the request."""
                return 200

            async def json(self):
                """JSON response."""
                return {
                    "meta": {
                        "deleted": {
                            "aliases": None,
                            "command": [
                                "d23779ce-4522-431d-9095-7bf34718c39d"
                            ],
                            "repeats": None
                        }
                    }
                }
        return Response()

command = Meta(MockAPI())

@pytest.mark.asyncio
async def test_command_add():
    """Add a command."""
    packet = MessagePacket(("text", "lol"), ("emoji", ""), role=5)
    assert (await command("add", "testing", packet, packet=packet)) == "Updated command !testing."

@pytest.mark.asyncio
async def test_command_remove():
    """Remove a command."""

    packet = MessagePacket("!command remove testing", role=5)
    assert (await command("remove", "testing", packet=packet)
           ) == "Removed command !testing."

@pytest.mark.asyncio
async def test_command_list():
    """List commands."""

    packet = MessagePacket("!command list", role=5)
    assert (await command("list", packet=packet)) == "Commands: testing"

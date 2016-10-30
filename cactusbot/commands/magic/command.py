"""Manage commands."""

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


from . import Command


class Meta(Command):
    """Manage commands."""

    COMMAND = "command"

    permissions = {
        '+': "Mod",
        '$': "Subscriber"
    }

    @Command.subcommand
    async def add(self, name: r'!?([+$]?)(.+)', *response,
                  added_by: "username"):
        """Add a command."""

        permissions = ','.join(self.permissions[symbol] for symbol in name[0])

        response = await self.api.add_command(
            name[1], ' '.join(response), permissions=permissions,
            added_by=added_by
        )

        # FIXME
        if response.status == 201:
            return "Added command !{}.".format(name[1])
        if response.status == 202:
            return "Updated command !{}.".format(name[1])
        raise Exception

    @Command.subcommand
    async def remove(self, name: "?command", *, removed_by: "username"):
        """Remove a command."""
        removed = await self.api.remove_command(name, removed_by=removed_by)
        if removed:
            return "Removed command !{}.".format(name)
        return "Command !{} does not exist!".format(name)

    @Command.subcommand
    async def list(self):
        """List all custom commands."""
        commands = await self.api.get_command()
        if commands:
            return "Commands: {}.".format(
                ', '.join(command["name"] for command in commands)
            )
        return "No commands added."

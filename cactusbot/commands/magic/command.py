"""Manage commands."""


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

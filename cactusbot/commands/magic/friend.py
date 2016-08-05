"""Manage friends."""


from . import Command



# TODO: Finish this command.
class Friend(Command):
    """Manage friends."""

    COMMAND = "friend"

    @Command.subcommand(hidden=False)
    async def get(self):
        """Get all the friends of the channel."""
        print(await self.api.get_friend())
        return "a"

    @Command.subcommand(hidden=False)
    async def add(self, *args: False):
        """Add a friend to the current channel."""

        if not args:
            return "You need to supply a user to add as a friend!"
        print(await self.api.add_friend(args))
        return "a"

    @Command.subcommand(hidden=False)
    async def remove(self, *args: False):
        """Remove a friend from the current channel."""
        if not args:
            return "You need to supply a user to remove as a friend!"
        print(await self.api.remove_friend(args))
        return "a"

    DEFAULT = get

"""Manage a users points."""

from . import Command


class Points(Command):
    """Manage friends."""

    COMMAND = "points"

    @Command.subcommand(hidden=False)
    async def get(self):
        """Get the users points."""
        return ""

    @Command.subcommand(hidden=False)
    async def give(self, *args: False):
        """Give a user points."""
        return ""

    @Command.subcommand(hidden=False)
    async def take(self, *args: False):
        """Take points from a user."""
        return ""

    DEFAULT = get

"""Interact with CactusAPI."""

from .services.api import API


class CactusAPI(API):
    """Interact with CactusAPI."""

    URL = "http://localhost:8000/api/v1/"

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)

        self.user = user

    # FIXME: match API
    async def add_command(self, name, response, *, permissions={},
                          added_by=None):
        """Add a command."""
        data = {
            "response": response,
        }
        return await self.patch("/user/{user}/command/{command}".format(
            user=self.user, command=name), data=data)

    # FIXME" match API
    async def remove_command(self, name, *, removed_by=None):
        """Remove a command."""
        data = {
            "removedBy": removed_by
        }
        return await self.delete("/user/{user}/command/{command}".format(
            user=self.user, command=name), data=data)

    async def get_command(self, name=None):
        """Get a command."""
        if name is not None:
            return await self.get("/user/{user}/command/{command}".format(
                user=self.user, command=name))
        return await self.get("/user/{user}/command".format(user=self.user))

    async def add_quote(self, quote, *, added_by=None):
        """Add a quote."""
        return "In development."

    async def remove_quote(self, quote_id):
        """Remove a quote."""
        return "In development."

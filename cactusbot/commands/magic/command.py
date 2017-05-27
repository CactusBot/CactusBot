"""Manage commands."""

from . import Command
from ..command import ROLES

_ROLE_NAMES = [ROLES[role].lower() for role in ROLES]
_REVERSED_ROLES = {v: k for k, v in ROLES.items()}


def _role_id(role_name):
    """Get the ID of a role from the name."""
    return _REVERSED_ROLES[role_name] if role_name in _REVERSED_ROLES else None


def _is_role(role):
    """Does a role name exist?"""
    return role.lower() in _ROLE_NAMES


async def _update_role(api, command, role):
    """Update the role of a command."""

    data = {
        "response": {
            "role": role
        }
    }

    return await api.command.update(command, data)


class Meta(Command):
    """Manage commands."""

    COMMAND = "command"
    ROLE = "moderator"

    ROLES = {
        '+': 4,
        '$': 2
    }

    @Command.command()
    async def add(self, command: r'!?([+$]?)([\w-]{1,32})', *response,
                  raw: "packet"):
        """Add a command."""

        symbol, name = command

        user_level = self.ROLES.get(symbol, 1)

        raw = raw.copy(role=user_level, target=None)

        response = await self.api.command.add(
            name, raw.split(maximum=3)[-1].json, user_level=user_level)
        data = await response.json()

        if data["meta"].get("created"):
            return "Added command !{}.".format(name)
        return "Updated command !{}.".format(name)

    @Command.command()
    async def remove(self, name: "?command"):
        """Remove a command."""
        response = await self.api.command.remove(name)
        if response.status == 200:
            return "Removed command !{}.".format(name)
        return "Command !{} does not exist!".format(name)

    @Command.command(name="list")
    async def list_commands(self):
        """List all custom commands."""
        response = await self.api.command.get()

        if response.status == 200:
            commands = (await response.json())["data"]

            return "Commands: {}".format(', '.join(sorted(
                command["attributes"]["name"] for command in commands
                if command.get("type") in (
                    "command", "builtin", "builtins", "alias")
            )))
        return "No commands added!"

    @Command.command()
    async def enable(self, command: "?command"):
        """Enable a command."""

        response = await self.api.command.toggle(command, True)
        if response.status == 200:
            return "Command !{} has been enabled.".format(command)

    @Command.command()
    async def disable(self, command: "?command"):
        """Disable a command."""

        response = await self.api.command.toggle(command, False)
        if response.status == 200:
            return "Command !{} has been disabled.".format(command)

    @Command.command()
    async def count(self, command: r'?command',
                    action: r"([=+-]?)(\d+)" = None):
        """Update the count of a command."""

        if action is None:
            response = await self.api.command.get(command)
            data = await response.json()
            if response.status == 404:
                return "Command !{} does not exist.".format(command)
            elif response.status == 200:
                return "!{command}'s count is {count}.".format(
                    command=command, count=data["data"]["attributes"]["count"])

        operator, value = action
        action_string = (operator or '=') + value

        response = await self.api.command.update_count(command, action_string)
        if response.status == 200:
            return "Count updated."

    @Command.command(role="moderator")
    async def permission(self, command: r'?command', role=None):
        """Change the role of a command."""

        if role is None:
            # Didn't get a value, return the role of the command
            response = await self.api.command.get(command)

            if response.status == 200:
                data = await response.json()
                minimum_role = data["data"]["attributes"]["response"]["role"]
                return "Minimum role for !{command} is '{role}'".format(
                    command=command, role=ROLES[minimum_role])

        valid_role = _is_role(role)
        if not valid_role:
            # Not a real role, tell the user.
            return "'{role}' is not a valid role!".format(role=role)

        # Valid role, update it.
        role_id = _role_id(role)
        if role_id is None:
            return "Invalid role {}".format(role)

        response = await _update_role(self.api, command, role_id)
        if response.status == 200:
            return "Updated role for !{command} to '{role}'".format(
                command=command, role=role)
        return "An error occurred."

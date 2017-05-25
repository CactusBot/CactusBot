"""Handle commands."""

import random

from ..commands import COMMANDS
from ..commands.command import ROLES
from ..handler import Handler
from ..packets import MessagePacket


class CommandHandler(Handler):
    """Command handler."""

    ARGN_EXPR = r'%ARG(\d+)(?:=([^|]+))?(?:((?:\|\w+)+))?%'
    ARGS_EXPR = r'%ARGS(?:=([^|]+))?((?:\|\w+)+)?%'
    MODIFIERS = {
        "upper": str.upper,
        "lower": str.lower,
        "title": str.title,
        "reverse": lambda text: text[::-1],
        "tag": lambda tag: tag[1:] if len(tag) > 1 and tag[0] == '@' else tag,
        "shuffle": lambda text: ''.join(random.sample(text, len(text)))
    }

    def __init__(self, channel, api):
        super().__init__()

        self.channel = channel

        self.api = api
        self.magics = {command.COMMAND: command(api) for command in COMMANDS}

    async def on_message(self, packet):
        """Handle message events."""

        if packet.target and packet.text == "/cry":
            return MessagePacket(
                "cries with ", ("tag", packet.user), action=True)

        if len(packet) > 1 and packet[0] == "!" and packet[1] != ' ':

            command, *args = packet[1:].text.split()

            data = {
                "username": packet.user,
                "channel": self.channel,
                "packet": packet
            }

            if command in self.magics:

                response = await self.magics[command](*args, **data)

                if packet.target and response:
                    if not isinstance(response, MessagePacket):
                        response = MessagePacket(response)
                    response.target = packet.user

                return response

            else:

                split = packet.split()[:-1]
                hyphenated_options = (((split[:index]), split[index:])
                                      for index in range(len(split), 0, -1))

                for command, args in hyphenated_options:

                    command = MessagePacket.join(*command,
                                                 separator='-').text[1:]
                    args = tuple(arg.text for arg in args)

                    response = await self.custom_response(
                        packet, command, *args, **data)

                    if response is not None:
                        return response

                return MessagePacket("Command not found.", target=packet.user)

    async def custom_response(self, _packet, command, *args, **data):
        """Custom command response to a packet."""

        args = (command, *args)

        response = await self.api.command.get(command)

        if response.status != 200:
            return

        json = await response.json()
        is_alias = False

        if json["data"].get("type") == "alias":

            is_alias = True

            command = json["data"]["attributes"]["commandName"]

            if "arguments" in json["data"]["attributes"]:
                args = (args[0], *tuple(MessagePacket(
                    *json["data"]["attributes"]["arguments"]
                ).text.split()), *args[1:])
        cmd = await self.api.command.get(name=command)
        if cmd.status != 200:
            return MessagePacket("Command does not exist for that alias.",
                                 target=_packet.user)
        cmd_response = await cmd.json()
        json["data"]["attributes"]["response"] = cmd_response[
            "data"]["attributes"]["response"]

        json = json["data"]["attributes"]

        if not json.get("enabled", True):
            return MessagePacket("Command is disabled.", target=_packet.user)

        if _packet.role < json["response"]["role"]:
            # pylint: disable=C0201
            return MessagePacket(
                "Role level '{role}' or higher required.".format(
                    role=ROLES[max(
                        k for k in ROLES.keys()
                        if k <= json["response"]["role"]
                    )]
                ),
                target=_packet.user if _packet.target else None
            )

        if _packet.target:
            json["response"]["target"] = _packet.user

        await self.api.command.update_count(command, "+1")
        if not is_alias and "count" not in data:
            data["count"] = str(json["count"] + 1)
        elif is_alias:
            data["count"] = str(cmd_response["data"]["attributes"]["count"])

        return self._inject(MessagePacket.from_json(json["response"]),
                            *args, **data)

    def _inject(self, _packet, *args, **data):
        """Inject targets into a packet."""

        def sub_argn(match):
            """Substitute an argument in place of an ARGN target."""

            argn, default, modifiers = match.groups()
            argn = int(argn)

            if default is None:
                result = args[argn]
            else:
                result = args[argn] if argn < len(args) else default

            if modifiers is not None:
                result = self.modify(result, *modifiers.split('|')[1:])

            return result

        try:
            _packet.sub(self.ARGN_EXPR, sub_argn)
        except IndexError:
            return MessagePacket("Not enough arguments!")

        def sub_args(match):
            """Substitute all arguments in place of the ARGS target."""

            default, modifiers = match.groups()

            if not args[1:] and default is not None:
                result = default
            else:
                if not args[1:]:
                    raise IndexError
                result = ' '.join(args[1:])

            if modifiers is not None:
                result = self.modify(result, *modifiers.split('|')[1:])

            return result

        try:
            _packet.sub(self.ARGS_EXPR, sub_args)
        except IndexError:
            return MessagePacket("Not enough arguments!")

        username = ""

        if "token" in data:
            username = data["token"]
        else:
            username = data.get("username")

        _packet.replace(**{
            "%USER%": username,
            "%COUNT%": data.get("count"),
            "%CHANNEL%": data.get("channel")
        })

        return _packet

    def modify(self, argument, *modifiers):
        """Apply modifiers to an argument."""

        for modifier in modifiers:
            if modifier in self.MODIFIERS:
                argument = self.MODIFIERS[modifier](argument)

        return argument

    async def on_repeat(self, packet):
        """Repeat event."""
        return packet

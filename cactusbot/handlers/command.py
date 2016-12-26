"""Handle commands."""

import random

from ..api import CactusAPI
from ..commands import COMMANDS
from ..handler import Handler
from ..packets import MessagePacket


class CommandHandler(Handler):
    """Command handler."""

    ARGN_EXPR = r'%ARG(\d+)(?:=([^|]+))?(?:((?:\|\w+)+))?%'
    ARGS_EXPR = r'%ARGS(?:=([^|]+))?(?:((?:\|\w+)+))?%'
    MODIFIERS = {
        "upper": str.upper,
        "lower": str.lower,
        "title": str.title,
        "reverse": lambda text: text[::-1],
        "tag": lambda tag: tag[1:] if tag[0] == '@' and len(tag) > 1 else tag,
        "shuffle": lambda text: ''.join(random.sample(text, len(text)))
    }

    def __init__(self, channel):
        super().__init__()

        self.channel = channel
        self.api = CactusAPI(channel.lower())  # FIXME

        self.magics = {command.COMMAND: command for command in COMMANDS}
        for command in self.magics.values():
            command.api = self.api

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

                response = await self.api.get_command(command)

                if response.status == 404:
                    response = await self.api.get_command_alias(command)

                    if response.status == 404:
                        return MessagePacket("Command not found.",
                                             target=packet.user)

                json = (await response.json()
                       )["data"]["attributes"]["response"]
                return self._inject(MessagePacket(
                    *json.pop("message"),
                    **{
                        **json,
                        "target": packet.user if packet.target else None
                    }
                ), command, *args, **data)

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
                result = self._modify(result, *modifiers.split('|')[1:])

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
                result = ' '.join(args[1:])

            if modifiers is not None:
                result = self._modify(result, *modifiers.split('|')[1:])

            return result

        if "%ARGS%" in _packet and len(args) < 2:
            return MessagePacket("Not enough arguments!")

        _packet.sub(self.ARGS_EXPR, sub_args)

        _packet.replace(**{
            "%USER%": data.get("username"),
            "%COUNT%": "%COUNT%",  # TODO
            "%CHANNEL%": data.get("channel")
        })

        return _packet

    def _modify(self, argument, *modifiers):
        """Apply modifiers to an argument."""

        for modifier in modifiers:
            if modifier in self.MODIFIERS:
                argument = self.MODIFIERS[modifier](argument)

        return argument

    async def on_repeat(self, packet):
        return packet

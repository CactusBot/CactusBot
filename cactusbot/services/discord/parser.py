import re

from ...packets import EditPacket, MessagePacket


class DiscordParser:

    # TODO: roles
    ROLES = {}

    MESSAGE_EXPR = [
        ("tag", r'<@(\d{17})>'),
        ("channel", r'<#(\d{18})>'),
        ("url", r'(https?://\w[^ ]+)'),
        ("emoji", u'([\U0001f600-\U0001f650])'),
        ("emoji", r'<(:\w{2,32}:)\d{18}>')
    ]

    @classmethod
    def parse_message(cls, packet):

        message = (packet.content,)
        for kind, expr in cls.MESSAGE_EXPR:
            message = cls._parse_message_expr(expr, kind, *message)
        message = list(message)

        for index, component in enumerate(message):
            if isinstance(component, str):
                message[index] = {
                    "type": "text",
                    "data": component,
                    "text": component
                }

        details = {
            "tag": ('@', packet.mentions),
            "channel": ('#', packet.channel_mentions)
        }

        for kind, (prefix, data) in details.items():
            index = 0
            for component in message:
                if component["type"] == kind:
                    component["text"] = prefix + data[index].name
                    index += 1

        # TODO: emoji conversion

        return MessagePacket(
            *message,
            user=packet.author.name,
            role=1,  # TODO
            action=packet.content.startswith(
                '*') and packet.content.endswith('*'),
            target=packet.channel.is_private
        )

    @classmethod
    def _parse_message_expr(cls, expr, kind, *data):
        for chunk in data:
            if isinstance(chunk, str):
                for index, value in enumerate(re.split(expr, chunk)):
                    if index % 2 == 1:
                        yield {
                            "type": kind,
                            "data": value,
                            "text": value
                        }
                    elif value:
                        yield value
            else:
                yield chunk

    @classmethod
    def parse_edit(cls, old, new):
        return EditPacket(cls.parse_message(old), cls.parse_message(new))

    @classmethod
    def synthesize(cls, packet):
        message = ""

        for component in packet:
            if component["type"] == "url":
                message += component["data"]
            else:
                message += component["text"]

        if packet.action:
            message = '*' + message + '*'

        if packet.target:
            pass  # TODO

        return message

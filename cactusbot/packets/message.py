"""Message packet."""

import re
from collections import namedtuple

from ..packet import Packet

MessageComponent = namedtuple("Component", ("type", "data", "text"))


class MessagePacket(Packet):
    """Message packet."""

    def __init__(self, *message, user="", role=1, action=False, target=None):
        super().__init__()

        message = list(message)
        for index, chunk in enumerate(message):
            if isinstance(chunk, dict):
                message[index] = MessageComponent(**chunk)
            elif isinstance(chunk, tuple):
                if len(chunk) == 2:
                    chunk = chunk + (chunk[1],)
                message[index] = MessageComponent(*chunk)
            elif isinstance(chunk, str):
                message[index] = MessageComponent("text", chunk, chunk)
        self.message = message

        self.user = user
        self.role = role
        self.action = action
        self.target = target

    def __str__(self):
        return "<Message: {} - \"{}\">".format(self.user, self.text)

    def __len__(self):
        return len(''.join(
            chunk.text for chunk in self.message
            if chunk.type == "text"
        ))

    def __getitem__(self, key):

        if isinstance(key, int):
            return ''.join(
                chunk.text for chunk in self.message
                if chunk.type == "text"
            )[key]

        elif isinstance(key, slice):

            if key.stop is not None or key.step is not None:
                raise NotImplementedError  # TODO

            count = key.start or 0
            message = self.message.copy()

            for index, component in enumerate(message.copy()):
                if component.type == "text":
                    if len(component.text) <= count:
                        count -= len(component.text)
                        message.pop(0)
                    else:
                        while count > 0:
                            new_text = component.text[1:]
                            component = message[index] = component._replace(
                                text=new_text, data=new_text)
                            count -= 1
                else:
                    message.pop(0)
                if count == 0:
                    return self.copy(*message)
            return self.copy(*message)

        raise TypeError

    def __contains__(self, item):
        for chunk in self.message:
            if chunk.type == "text" and item in chunk.text:
                return True
        return False

    def __iter__(self):
        return self.message.__iter__()

    @property
    def text(self):
        """Pure text representation of the packet."""
        return ''.join(chunk.text for chunk in self.message)

    @property
    def json(self):
        """JSON representation of the packet."""
        return {
            "message": [
                dict(component._asdict()) for component in self.message
            ],
            "user": self.user,
            "role": self.role,
            "action": self.action,
            "target": self.target
        }

    def copy(self, *args, **kwargs):
        """Return a copy."""

        _args = args or self.message

        _kwargs = {
            "user": self.user,
            "role": self.role,
            "action": self.action,
            "target": self.target
        }
        _kwargs.update(kwargs)

        return MessagePacket(*_args, **_kwargs)

    def replace(self, **values):
        """Replace text in packet."""
        for index, chunk in enumerate(self.message):
            if chunk.type == "text":
                for old, new in values.items():
                    if new is not None:
                        self.message[index] = self.message[index]._replace(
                            text=chunk.text.replace(old, new))
                        chunk = self.message[index]
        return self

    def sub(self, pattern, repl):
        """Perform regex substitution on packet."""
        for index, chunk in enumerate(self.message):
            if chunk.type in ("text", "link"):
                self.message[index] = self.message[index]._replace(
                    text=re.sub(pattern, repl, chunk.text))
        return self

    def split(self, seperator=' ', maximum=None):
        """Split into multiple MessagePackets, based on a separator."""

        result = []
        components = []

        if maximum is None:
            maximum = float('inf')

        for component in self:

            if len(result) == maximum:
                components.append(component)
                continue

            is_text = component.type == "text"
            if not is_text or seperator not in component.text:
                components.append(component)
                continue

            new = MessageComponent("text", "", "")

            for index, character in enumerate(component.text):
                if len(result) == maximum:
                    new_text = new.text + component.text[index:]
                    new = new._replace(data=new_text, text=new_text)
                    break

                if character == seperator:
                    components.append(new._replace())
                    result.append(components.copy())
                    components.clear()
                    new = new._replace(data="", text="")
                else:
                    new_text = new.text + character
                    new = new._replace(data=new_text, text=new_text)

            components.append(new)

        result.append(components)

        return [self.copy(*filter(lambda c: c.text, message))
                for message in result]

    @classmethod
    def from_json(cls, json):
        return cls(*json.pop("message"), **json)

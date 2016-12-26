"""Edit packet."""

from ..packet import Packet


class EditPacket(Packet):

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def __str__(self):
        return "<Edit: {}>".format(self.new)

    @property
    def json(self):
        return {
            "old": self.old,
            "new": self.new
        }

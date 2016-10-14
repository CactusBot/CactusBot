"""Handle events"""

from ..handler import Handler
from ..packets import MessagePacket
from ..cached import CacheUtils
import time
import calendar


class EventHandler(Handler):
    """Events handler."""

    def __init__(self, config_data):
        super().__init__()

        self.cache = CacheUtils("caches/followers.json")
        self.cache_follows = config_data["CACHE_FOLLOWS"]
        self.follow_time = config_data["CACHE_FOLLOWS_TIME"] * 60
        self.follow_message = config_data["FOLLOW_MESSAGE"]
        self.sub_message = config_data["SUB_MESSAGE"]
        self.host_message = config_data["HOST_MESSAGE"]

    def on_follow(self, packet):
        """Handle follow packets."""
        def on_follow_return():
            return MessagePacket(self.follow_message.format(packet.user))

        if packet.success:
            if self.cache_follows:
                if self.cache.in_cache(packet.user):
                    if self.follow_time > 0:
                        cache_time = self.cache.return_data(packet.user)
                        if cache_time + self.follow_time <= time.time():
                            self.cache.cache_add(packet.user)
                            return on_follow_return()
                else:
                    self.cache.cache_add(packet.user)
                    return on_follow_return()
            else:
                return on_follow_return()

    def on_subscribe(self, packet):
        """Handle subscription packets."""
        # TODO: Make configurable
        return MessagePacket(self.sub_message.format(packet.user))

    def on_host(self, packet):
        """Handle host packets."""
        # TODO: Make configurable
        return MessagePacket(self.host_message.format(packet.user))

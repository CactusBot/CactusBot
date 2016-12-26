"""CactusBot configuration."""

from cactusbot.handler import Handlers
from cactusbot.handlers import (CommandHandler, EventHandler, LoggingHandler,
                                SpamHandler)
from cactusbot.services.beam.handler import BeamHandler

AUTH = ("BotUsername", "BotPassword")

CHANNEL = "ChannelName"

API_TOKEN = "CactusAPI_Token"

# CACHE_FOLLOWS: Cache to remove chat spam (Default: False)
# CACHE_FOLLOWS_TIME: How long in minutes before resending message
#   Leave at 0 for no repeat follow messages
#   Only matters if CACHE_FOLLOWS is enabled (Default: 0)
CACHE_DATA = {
    "CACHE_FOLLOWS": True,
    "CACHE_FOLLOWS_TIME": 0
}

handlers = Handlers(LoggingHandler(), EventHandler(CACHE_DATA),
                    CommandHandler(CHANNEL), SpamHandler())

SERVICE = BeamHandler(CHANNEL, handlers)

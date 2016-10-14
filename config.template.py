"""CactusBot configuration."""

from cactusbot.services.beam.handler import BeamHandler

from cactusbot.handler import Handlers
from cactusbot.handlers import (CommandHandler, LoggingHandler,
                                SpamHandler, EventHandler)


USERNAME = "BotUsername"
PASSWORD = "BotPassword"

CHANNEL = "TargetName"

# CACHE_FOLLOWS: Cache to remove chat spam (Default: False)
# CACHE_FOLLOWS_TIME: How long in minutes before resending message
#   Leave at 0 for no repeat follow messages
#   Only matters if CACHE_FOLLOWS is enabled (Default: 0)
# FOLLOWS_MESSAGE: Message to be sent when somebody follows the channel
#   {0} in the message will be replaced by the user
#   Same functionality with SUB_MESSAGE and HOST_MESSAGE
CONFIG_DATA = {
                "CACHE_FOLLOWS": False,
                "CACHE_FOLLOWS_TIME": 0,

                "FOLLOW_MESSAGE": "Thanks for following, @{0} !",
                "SUB_MESSAGE": "Thanks for subscribing, @{0} !",
                "HOST_MESSAGE": "Thanks for hosting, @{0} !"
}

handlers = Handlers(LoggingHandler(), EventHandler(CONFIG_DATA),
                    CommandHandler(CHANNEL), SpamHandler())

SERVICE = BeamHandler(CHANNEL, handlers)

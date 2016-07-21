"""CactusBot configuration."""

from cactusbot.services import BeamHandler

USERNAME = "BotUsername"
PASSWORD = "p455w0rd"

CHANNEL = "ChannelName"

SERVICE = BeamHandler(CHANNEL)

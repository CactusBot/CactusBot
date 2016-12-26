import pytest

from cactusbot.handlers import CommandHandler
from cactusbot.packets import MessagePacket

command_handler = CommandHandler("TestChannel")


def verify(message, expected, *args, **kwargs):
    """Verify target substitutions."""
    actual = command_handler._inject(
        MessagePacket(
            *message if isinstance(message, list) else (message,)),
        *args, **kwargs
    ).text
    assert actual == expected


@pytest.mark.asyncio
async def test_on_message():
    assert (await command_handler.on_message(
        MessagePacket("!cactus")
    )).text == "Ohai! I'm CactusBot! 🌵"


def test_inject_argn():

    verify(
        "Let's raid %ARG1%!",
        "Let's raid GreatStreamer!",
        "raid", "GreatStreamer"
    )

    verify(
        "Let's raid %ARG1%! #%ARG2%",
        "Let's raid GreatStreamer! #ChannelRaid",
        "raid", "GreatStreamer", "ChannelRaid"
    )

    verify(
        "Let's raid %ARG1%!",
        "Not enough arguments!",
        "raid"
    )

    verify(
        "This is the !%ARG0% command.",
        "This is the !test command.",
        "test", "arg1", "arg2"
    )

    verify(
        "%ARG1|upper% IS AMAZING!",
        "SALAD IS AMAZING!",
        "amazing", "salad", "taco"
    )

    verify(
        "If you reverse %ARG1%, you get %ARG1|reverse%!",
        "If you reverse potato, you get otatop!",
        "reverse", "potato"
    )

    verify(
        ["Let's raid %ARG1%! ", ("link", "beam.pro/%ARG1|tag%")],
        "Let's raid @Streamer! beam.pro/Streamer",
        "raid", "@Streamer"
    )


def test_inject_args():

    verify(
        "Have some %ARGS%!",
        "Have some hamster-powered floofle waffles!",
        "gift", *"hamster-powered floofle waffles".split()
    )

    verify(
        "Have some %ARGS%.",
        "Not enough arguments!",
        "give"
    )


def test_inject_user():

    verify(
        "Ohai, %USER%!",
        "Ohai, SomeUser!",
        "ohai", username="SomeUser"
    )

    verify(
        "Ohai, %USER%!",
        "Ohai, %USER%!",
        "ohai"
    )


def test_inject_count():
    pass


def test_inject_channel():

    verify(
        "Welcome to %CHANNEL%'s stream!",
        "Welcome to GreatStreamer's stream!",
        "welcome", channel="GreatStreamer"
    )

    verify(
        "Welcome to %CHANNEL%'s stream!",
        "Welcome to %CHANNEL%'s stream!",
        "welcome"
    )

import pytest

from cactusbot.handlers import EventHandler
from cactusbot.packets import EventPacket

event_handler = EventHandler({
    "CACHE_FOLLOWS": False,
    "CACHE_FOLLOWS_TIME": 0
})


@pytest.mark.asyncio
async def test_on_message():

    assert (await event_handler.on_start(
        None
    )).text == "CactusBot activated. 🌵"


@pytest.mark.asyncio
async def test_on_follow():

    assert (await event_handler.on_follow(EventPacket(
        "follow", "TestUser"
    ))).text == "Thanks for following, TestUser!"

    assert (await event_handler.on_follow(EventPacket(
        "follow", "TestUser", success=False
    ))) is None


@pytest.mark.asyncio
async def test_on_subscribe():

    assert (await event_handler.on_subscribe(EventPacket(
        "subscribe", "TestUser"
    ))).text == "Thanks for subscribing, TestUser!"


@pytest.mark.asyncio
async def test_on_host():

    assert (await event_handler.on_host(EventPacket(
        "host", "TestUser"
    ))).text == "Thanks for hosting, TestUser!"

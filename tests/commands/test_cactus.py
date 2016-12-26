import pytest

from cactusbot.commands.magic import Cactus


@pytest.mark.asyncio
async def test_default():
    assert (await Cactus()).text == "Ohai! I'm CactusBot! 🌵"


@pytest.mark.asyncio
async def test_docs():
    assert (await Cactus("docs")).text == ("Check out my documentation at "
                                           "cactusbot.rtfd.org.")


@pytest.mark.asyncio
async def test_twitter():
    assert (await Cactus("twitter")).text == (
        "You can follow the team behind CactusBot at: "
        "twitter.com/CactusDevTeam")


@pytest.mark.asyncio
async def test_github():
    assert (await Cactus("github")).text == (
        "Check out my GitHub repository at: github.com/CactusDev/CactusBot")
    assert (await Cactus("github", "cactusbot")).text == (
        "Check out my GitHub repository at: github.com/CactusDev/CactusBot")
    assert (await Cactus("github", "CactusDev")).text == (
        "Check out the CactusDev GitHub organization at: github.com/CactusDev")
    assert (await Cactus("github", "issue")).text == (
        "Create a GitHub issue at: github.com/CactusDev/CactusBot/issues")
    assert (await Cactus("github", "CactusAPI")).text == (
        "Check out the GitHub repository for CactusAPI at: "
        "github.com/CactusDev/CactusAPI")
    assert (await Cactus("github", "SEPAL")).text == (
        "Check out the GitHub repository for Sepal at: "
        "github.com/CactusDev/Sepal")
    assert (await Cactus("github", "assets")).text == (
        "Check out the CactusDev assets at: github.com/CactusDev/CactusAssets")
    assert (await Cactus("github", "nonexistant")).text == (
        "Unknown project 'nonexistant'.")


@pytest.mark.asyncio
async def test_help():
    assert (await Cactus("help")) == (
        "Try our docs (!cactus docs). "
        "If that doesn't help, tweet at us (!cactus twitter)!")

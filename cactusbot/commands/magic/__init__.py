"""Define custom magic commands."""

from .. import Command

from .command import Meta
from .quote import Quote
from .cube import Cube, Temmie
from .social import Social
from .friend import Friend

COMMANDS = (Meta, Quote, Cube, Temmie, Social, Friend)

__all__ = ["Command", "Meta", "Quote", "Cube", "Friend"]

"""Define custom magic commands."""

from .. import Command

from .command import Meta
from .quote import Quote
from .cube import Cube, Temmie

COMMANDS = (Meta, Quote, Cube, Temmie)

__all__ = ["Command", "Meta", "Quote", "Cube"]

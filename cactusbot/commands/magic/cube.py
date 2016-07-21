"""Cube things."""

import re

from random import choice
from difflib import get_close_matches

from . import Command


class Cube(Command):
    """Cube things."""

    COMMAND = "cube"

    NUMBER_EXPR = re.compile(r'^[-+]?\d*\.\d+|[-+]?\d+$')

    @Command.subcommand(hidden=True)
    async def run(self, *args: False, username: "username") -> "cube":
        """Cube things!"""

        if not args:
            return self.cube(username)
        if args == ('2',):
            return "8! Whoa, that's 2Cubed!"
        elif len(args) > 8:
            return "Whoa! That's 2 many cubes!"

        return ' · '.join(self.cube(arg) for arg in args)

    def cube(self, value: str):
        """Cube a value."""

        if value.startswith(':'):  # HACK: global emote parsing required
            return '{} ³'.format(value)

        match = re.match(self.NUMBER_EXPR, value)
        if match is not None:
            return '{:.4g}'.format(float(match.string)**3)

        return '({})³'.format(value)

    DEFAULT = run


class Temmie(Command):
    "awwAwa!!"

    COMMAND = "temmie"

    quotes = [
        "fhsdhjfdsfjsddshjfsd",
        "hOI!!!!!! i'm tEMMIE!!",
        "awwAwa cute!! (pets u)",
        "OMG!! humans TOO CUTE (dies)",
        "NO!!!!! muscles r... NOT CUTE",
        "NO!!! so hungr... (dies)",
        "FOOB!!!",
        "can't blame a BARK for tryin'...",
        ("/me RATED TEM OUTTA TEM. Loves to pet cute humans. "
         "But you're allergic!"),
        "/me Special enemy Temmie appears here to defeat you!!",
        "/me Temmie is trying to glomp you.",
        "/me Temmie forgot her other attack.",
        "/me Temmie is doing her hairs.",
        "/me Smells like Temmie Flakes.",
        "/me Temmie vibrates intensely.",
        "/me Temmiy accidentally misspells her own name.",
        "/me You flex at Temmie...",
        "/me Temmie only wants the Temmie Flakes.",
        "/me You say hello to Temmie."
    ]  # HACK: using /me, which is not global

    @Command.subcommand(hidden=True)
    async def get(self, query=None):
        """hOI!!!!!!"""
        if query is None:
            return choice(self.quotes)
        return get_close_matches(query, self.quotes, n=1, cutoff=0)[0]

    DEFAULT = get

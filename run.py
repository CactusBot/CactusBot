#!/usr/bin/env python3.5

"""Run CactusBot."""

from asyncio import get_event_loop

from argparse import ArgumentParser

import logging

from cactusbot import Cactus

from config import SERVICE, AUTH


if __name__ == "__main__":

    parser = ArgumentParser(description="Run CactusBot.")

    parser.add_argument(
        "--debug",
        help="set custom logger level",
        metavar="LEVEL",
        nargs='?',
        const="DEBUG",
        default="INFO"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=args.debug,
        format="{asctime} {levelname} {name} {funcName}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style='{'
    )

    loop = get_event_loop()

    # TODO: Convert this to be able to have multiple services
    cactus = Cactus(SERVICE)

    try:
        # TODO: Make this cactus.run(services) instead of only Beam
        loop.run_until_complete(cactus.run(*AUTH))
        loop.run_forever()
    # TODO: Error catching?
    finally:
        loop.close()

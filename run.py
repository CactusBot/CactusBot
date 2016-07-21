"""Run CactusBot."""

from asyncio import get_event_loop

from argparse import ArgumentParser

import logging

from cactusbot import Cactus

from config import SERVICE, USERNAME, PASSWORD


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

    parser.add_argument(
        "--quiet",
        help="send no messages to public chat",
        metavar="USER",
        nargs='?',
        const=True,
        default=False
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=args.debug,
        format="{asctime} {levelname} {name} {funcName}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style='{'
    )

    loop = get_event_loop()

    cactus = Cactus(SERVICE)

    try:
        loop.run_until_complete(cactus.run(USERNAME, PASSWORD))
        loop.run_forever()
    finally:
        loop.close()

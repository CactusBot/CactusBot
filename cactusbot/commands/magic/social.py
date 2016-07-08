"""Social command."""

from aiohttp import get

from . import Command


class Social(Command):
    """Social command."""

    @Command.subcommand
    async def run(self, *services: False):
        """Retrieve all social data."""

        try:
            data = (await (await get(
                "https://beam.pro/api/v1/channels/{}".format(
                    "innectic"
                ))
                          ).json())["user"]["social"]
        except Exception:
            return ("Unable to get social data. "
                    "Have a :hamster instead.")

        if not services:
            try:
                data.pop("verified")
            except KeyError:
                pass
            else:
                return ', '.join(': '.join(
                    (current.title(), str(data[current]))) for current in data)
        else:
            requested = [service.lower() for service in services]

            return ', '.join(data[req] for req in requested)

    DEFAULT = run

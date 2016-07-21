"""CactusBot!"""

from logging import getLogger

import time

__version__ = "v0.4-dev"


# TODO: change to new logo
CACTUS_ART = r"""CactusBot initialized!

      ,`""',
      ;' ` ;
      ;`,',;
      ;' ` ;
 ,,,  ;`,',;               _____           _
;,` ; ;' ` ;   ,',        / ____|         | |
;`,'; ;`,',;  ;,' ;      | |     __ _  ___| |_ _   _ ___
;',`; ;` ' ; ;`'`';      | |    / _` |/ __| __| | | / __|
;` '',''` `,',`',;       | |___| (_| | (__| |_| |_| \__ \
 `''`'; ', ;`'`'          \_____\__,_|\___|\__|\__,_|___/
      ;' `';
      ;` ' ;
      ;' `';
      ;` ' ;
      ; ',';
      ;,' ';  {version}

Made by: 2Cubed, Innectic, and ParadigmShift3d
""".format(version=__version__)


class Cactus(object):
    """Run CactusBot safely."""

    def __init__(self, service, *, debug="INFO", quiet=False):
        super().__init__()

        self.logger = getLogger(__name__)

        self.service = service

        self.debug = debug  # XXX: find purpose or remove
        self.quiet = quiet  # TODO: implement

    async def run(self, username, password):
        """Run bot."""

        self.logger.info(CACTUS_ART)

        try:
            await self.service.run(username, password)

        except KeyboardInterrupt:
            self.logger.info("Removing thorns... done.")

        except Exception:
            self.logger.critical("Oh no, I crashed!", exc_info=True)

            self.logger.info("Restarting in 10 seconds...")

            try:
                time.sleep(10)
            except KeyboardInterrupt:
                self.logger.info("CactusBot deactivated.")

"""CactusBot!"""

"""
The MIT License

Copyright (c) 2016 CactusDev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

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

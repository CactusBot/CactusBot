"""Interact with a REST API."""

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

from urllib.parse import urljoin
from aiohttp import ClientSession, ClientHttpProcessingError


class API(ClientSession):
    """Interact with a REST API."""

    URL = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = getLogger(__name__)

    def _build(self, endpoint):
        return urljoin(self.URL, endpoint.lstrip('/'))

    async def request(self, method, endpoint, **kwargs):
        """Send HTTP request to an endpoint."""

        url = self._build(endpoint)

        async with super().request(method, url, **kwargs) as response:
            if not response.status == 200:
                error = "{resp.status} {resp.reason}".format(resp=response)
                self.logger.error(error)
                raise ClientHttpProcessingError(error)
            try:
                return await response.json()
            except ValueError:
                self.logger.warning("Response was not JSON!")
                raise ClientHttpProcessingError("Response was not JSON!")

    async def get(self, endpoint, **kwargs):
        return await self.request("GET", endpoint, **kwargs)

    async def options(self, endpoint, **kwargs):
        return await self.request("OPTIONS", endpoint, **kwargs)

    async def head(self, endpoint, **kwargs):
        return await self.request("HEAD", endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        return await self.request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        return await self.request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.request("DELETE", endpoint, **kwargs)

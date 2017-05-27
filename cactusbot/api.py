"""Interact with CactusAPI."""

import json

from .services.api import API


class CactusAPI(API):
    """Interact with CactusAPI."""

    URL = "https://cactus.exoz.one/api/v1/"

    SCOPES = {
        "alias:create", "alias:manage",
        "command:create", "command:manage",
        "config:create", "config:manage",
        "quote:create", "quote:manage",
        "repeat:create", "repeat:manage",
        "social:create", "social:manage",
        "trust:create", "trust:manage",
    }

    def __init__(self, token, password, url=URL, auth_token="", **kwargs):
        super().__init__(**kwargs)

        self.token = token
        self.auth_token = auth_token
        self.password = password
        self.url = url

        self.buckets = {
            "alias": Alias(self),
            "command": Command(self),
            "config": Config(self),
            "quote": Quote(self),
            "repeat": Repeat(self),
            "social": Social(self),
            "trust": Trust(self)
        }

    def __getattr__(self, attr):
        return self.buckets.get(attr)

    async def request(self, method, endpoint, **kwargs):
        """Send HTTP request to endpoint."""

        is_json = kwargs.pop("is_json", True)

        headers = {
            "X-Auth-Token": self.token,
            "X-Auth-Key": self.auth_token
        }

        if is_json:
            headers["Content-Type"] = "application/json"

        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        response = await super().request(method, endpoint, **kwargs)

        if response.status == 401:
            reauth = await self.login(self.password, *self.SCOPES)
            if reauth.status == 200:
                self.auth_token = (await reauth.json()).get("token")
                response = await super().request(method, endpoint, **kwargs)

        return response

    async def get(self, endpoint, **kwargs):
        """Perform a GET request without requesting a JSON response."""
        return await super().get(endpoint, is_json=False, **kwargs)

    async def login(self, *scopes, password=None):
        """Authenticate."""

        if password is None:
            password = self.password

        data = {
            "token": self.token,
            "password": password,
            "scopes": scopes
        }

        response = await self.post("/login", data=json.dumps(data))

        auth_response = await response.json()
        if response.status == 404:
            raise ValueError(auth_response["errors"])
        else:
            self.auth_token = auth_response.get("token")

        return response


class CactusAPIBucket:
    """CactusAPI bucket."""

    # pylint: disable=R0903

    def __init__(self, api):
        self.api = api


class Alias(CactusAPIBucket):
    """CactusAPI /alias bucket."""

    async def get(self, alias):
        """Get a command alias."""
        return await self.api.get("/user/{token}/alias/{alias}".format(
            token=self.api.token, alias=alias))

    async def add(self, command, alias, args=None):
        """Create a command alias."""

        data = {
            "commandName": command,
        }

        if args is not None:
            data["arguments"] = args

        return await self.api.patch("/user/{token}/alias/{alias}".format(
            token=self.api.token, alias=alias), data=json.dumps(data))

    async def remove(self, alias):
        """Remove a command alias."""

        return await self.api.delete("/user/{token}/alias/{alias}".format(
            token=self.api.token, alias=alias))


class Command(CactusAPIBucket):
    """CactusAPI /command bucket."""

    async def get(self, name=None):
        """Get a command."""

        if name is not None:
            return await self.api.get(
                "/user/{token}/command/{command}".format(
                    token=self.api.token, command=name))
        return await self.api.get("/user/{token}/command".format(
            token=self.api.token))

    async def add(self, name, response, *, user_level=1):
        """Add a command."""

        data = {
            "response": response,
            "userLevel": user_level
        }

        return await self.api.patch(
            "/user/{token}/command/{command}".format(
                token=self.api.token, command=name),
            data=json.dumps(data)
        )

    async def remove(self, name):
        """Remove a command."""

        return await self.api.delete("/user/{token}/command/{command}".format(
            token=self.api.token, command=name))

    async def toggle(self, command, state):
        """Toggle the enabled state of a command"""

        data = {"enabled": state}

        return await self.api.patch("/user/{token}/command/{command}".format(
            token=self.api.token, command=command), data=json.dumps(data))

    async def update_count(self, command, value):
        """Set the count of a command."""

        data = {"count": value}

        return await(
            self.api.patch("/user/{token}/command/{command}/count".format(
                token=self.api.token, command=command), data=json.dumps(data)))

    async def update(self, command, value):
        """Update command attributes."""

        return await self.api.patch("/user/{token}/command/{command}".format(
            token=self.api.token, command=command), data=json.dumps(value))


class Config(CactusAPIBucket):
    """CactusAPI /config bucket."""

    async def get(self, *keys):
        """Get the token config."""

        if keys:
            return await self.api.get("/user/{token}/config".format(
                token=self.api.token), data=json.dumps({"keys": keys}))

        return await self.api.get("/user/{token}/config".format(
            token=self.api.token))

    async def update(self, value):
        """Update config attributes."""

        return await self.api.patch("/user/{token}/config".format(
            token=self.api.token), data=json.dumps(value))


class Quote(CactusAPIBucket):
    """CactusAPI /quote bucket."""

    async def get(self, quote_id=None):
        """Get a quote."""

        if quote_id is not None:
            return await self.api.get("/user/{token}/quote/{id}".format(
                token=self.api.token, id=quote_id))
        return await self.api.get("/user/{token}/quote".format(
            token=self.api.token), params={"random": "true"})

    async def add(self, quote):
        """Add a quote."""

        data = {"quote": quote}

        return await self.api.post(
            "/user/{token}/quote".format(token=self.api.token),
            data=json.dumps(data)
        )

    async def edit(self, quote_id, quote):
        """Edit a quote."""

        data = {"quote": quote}

        return await self.api.patch(
            "/user/{token}/quote/{quote_id}".format(
                token=self.api.token, quote_id=quote_id),
            data=json.dumps(data)
        )

    async def remove(self, quote_id):
        """Remove a quote."""

        return await self.api.delete("/user/{token}/quote/{id}".format(
            token=self.api.token, id=quote_id))


class Repeat(CactusAPIBucket):
    """CactusAPI /repeat bucket."""

    async def get(self):
        """Get all repeats."""
        return await self.api.get("/user/{token}/repeat".format(
            token=self.api.token))

    async def add(self, command, period):
        """Add a repeat."""

        data = {
            "commandName": command,
            "period": period
        }

        return await self.api.patch("/user/{token}/repeat/{command}".format(
            token=self.api.token, command=command), data=json.dumps(data))

    async def remove(self, repeat):
        """Remove a repeat."""

        return await self.api.delete("/user/{token}/repeat/{repeat}".format(
            token=self.api.token, repeat=repeat))


class Social(CactusAPIBucket):
    """CactusAPI /social bucket."""

    async def get(self, service=None):
        """Get social service."""

        if service is None:
            return await self.api.get("/user/{token}/social".format(
                token=self.api.token))
        return await self.api.get("/user/{token}/social/{service}".format(
            token=self.api.token, service=service))

    async def add(self, service, url):
        """Add a social service."""

        data = {"url": url}

        return await self.api.patch("/user/{token}/social/{service}".format(
            token=self.api.token, service=service), data=json.dumps(data))

    async def remove(self, service):
        """Remove a social service."""

        return await self.api.delete("/user/{token}/social/{service}".format(
            token=self.api.token, service=service))


class Trust(CactusAPIBucket):
    """CactusAPI /trust bucket."""

    async def get(self, user_id=None):
        """Get trusted users."""

        if user_id is None:
            return await self.api.get("/user/{token}/trust".format(
                token=self.api.token))

        return await self.api.get("/user/{token}/trust/{user_id}".format(
            token=self.api.token, user_id=user_id))

    async def add(self, user_id, username):
        """Trust new user."""

        data = {"userName": username}

        return await self.api.patch("/user/{token}/trust/{user_id}".format(
            token=self.api.token, user_id=user_id), data=json.dumps(data))

    async def remove(self, user_id):
        """Remove user trust."""

        return await self.api.delete("/user/{token}/trust/{user_id}".format(
            token=self.api.token, user_id=user_id))

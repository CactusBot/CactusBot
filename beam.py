from logging import getLogger as get_logger
from logging import INFO, WARNING, FileHandler
from requests import Session
from json import dumps, loads
from websockets import connect


class Beam:
    path = "https://beam.pro/api/v1"

    message_id = 0

    def __init__(self, debug="WARNING", **kwargs):
        self._init_logger(debug, kwargs.get("log_to_file"))
        self.http_session = Session()
        self.config = kwargs.get("config", dict())

    def _init_logger(self, level, log_to_file=False):
        """Initialize logger."""

        self.logger = get_logger("CactusBot")

        if log_to_file:
            fh = FileHandler("latest.log")
            fh.setLevel(INFO)
            self.logger.addHandler(fh)

        level = level.upper()

        if level is True:
            level = "DEBUG"
        elif level is False:
            level = "WARNING"

        levels = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET")
        if level in levels:
            level_num = __import__("logging").__getattribute__(level)
            self.logger.setLevel(level_num)
            get_logger("urllib3").setLevel(WARNING)
            get_logger("websockets").setLevel(WARNING)
            self.logger.info("Logger level set to: {}".format(level))

            try:
                from coloredlogs import install
                install(level=level)
            except ImportError:
                self.logger.warning(
                    "Module 'coloredlogs' unavailable; using ugly logging.")
        else:
            self.logger.warn("Invalid logger level: {}".format(level))

        self.logger.info("Logger initialized!")

    def _request(self, req, url, **kwargs):
        """Send HTTP request to Beam."""
        if req.lower() in ("get", "head", "post", "put", "delete", "options"):
            if req.lower() == "get":
                response = self.http_session.get(
                    self.path + url,
                    params=kwargs.get("params")
                )
            else:
                response = self.http_session.__getattribute__(req.lower())(
                    self.path + url,
                    data=kwargs.get("data")
                )

            try:
                json = response.json()
            except ValueError:
                return None
            else:
                if "error" in json.keys():
                    self.logger.warn("Error: {}".format(json["error"]))
                return json
        else:
            self.logger.debug("Invalid request: {}".format(req))

    def login(self, username, password, code=""):
        """Authenticate and login with Beam."""
        l = locals()
        packet = {n: l[n] for n in ("username", "password", "code")}
        return self._request("POST", "/users/login", data=packet)

    def get_channel(self, id, **p):
        """Get channel data by username."""
        return self._request("GET", "/channels/{id}".format(id=id), params=p)

    def get_chat(self, id):
        """Get chat server data."""
        return self._request("GET", "/chats/{id}".format(id=id))

    def connect(self, channel_id, bot_id):
        """Connect to a Beam chat through a websocket."""

        chat = self.get_chat(channel_id)
        server = chat["endpoints"][0]
        authkey = chat["authkey"]

        self.logger.debug("Connecting to: {server}".format(server=server))

        self.websocket = yield from connect(server)

        response = yield from self.send_message(
            (channel_id, bot_id, authkey), method="auth"
        )

        response = loads(response)

        if response["data"]["authenticated"]:
            self.logger.debug(response)
            return self.websocket
        return False

    def send_message(self, arguments, method="msg"):
        """Send a message to a Beam chat through a websocket."""

        if isinstance(arguments, str):
            arguments = (arguments,)

        message_packet = {
            "type": "method",
            "method": method,
            "arguments": arguments,
            "id": self.message_id
        }

        yield from self.websocket.send(dumps(message_packet))
        self.message_id += 1

        if method in ("msg", "auth"):
            return (yield from self.websocket.recv())
        return True

    def remove_message(self, channel_id, message_id):
        """Remove a message from chat."""
        return self._request("DELETE", "/chats/{id}/message/{message}".format(
            id=channel_id, message=message_id))

    def read_chat(self, handle=None):
        while True:
            response = loads((yield from self.websocket.recv()))
            self.logger.debug(response)

            if handle:
                handle(response)
from tornado.websocket import websocket_connect
from tornado.gen import coroutine
from tornado.ioloop import PeriodicCallback

from tornado.gen import coroutine

from requests import Session
from requests.compat import urljoin

from logging import getLogger as get_logger
from logging import getLevelName as get_level_name
from logging import StreamHandler, FileHandler, Formatter

from functools import partial
import json

from re import match

class Twitch():

    def __init__(self, debug="INFO", **kwargs):
        self._init_logger(debug, kwargs.get("log_to_file", True))
        self.http_session = Session()

        with open('data/bots/bot.json', "r+") as config:
            bot = json.load(config)

        with open('data/config-template.json', "r+") as config:
            config = json.load(config)

        self.host = config["twitch"]["host"]
        self.port = config["twitch"]["port"]
        self.channel = bot["twitch"]["channel"]
        self.username = bot["twitch"]["username"]
        self.password = bot["twitch"]["password"]

        self.uri = "ws://" + self.host + ":" + str(self.port)

    def _init_logger(self, level="INFO", file_logging=True, **kwargs):
        """Initialize logger."""

        self.logger = get_logger("CactusBot")
        self.logger.propagate = False

        self.logger.setLevel("DEBUG")

        if level is True or level.lower() == "true":
            level = "DEBUG"
        elif level is False or level.lower() == "false":
            level = "WARNING"
        elif hasattr(level, "upper"):
            level = level.upper()

        format = kwargs.get(
            "format",
            "%(asctime)s %(name)s %(levelname)-8s %(message)s"
        )

        formatter = Formatter(format, datefmt='%Y-%m-%d %H:%M:%S')

        try:
            from coloredlogs import ColoredFormatter
            colored_formatter = ColoredFormatter(format)
        except ImportError:
            colored_formatter = formatter
            self.logger.warning(
                "Module 'coloredlogs' unavailable; using ugly logging.")

        stream_handler = StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(colored_formatter)
        self.logger.addHandler(stream_handler)

        if file_logging:
            file_handler = FileHandler("latest.log")
            file_handler.setLevel("DEBUG")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        get_logger("requests").setLevel(get_level_name("WARNING"))

        self.logger.info("Logger initialized with level '{}'.".format(level))

    def _request(self, url, method="GET", **kwargs):
        """Send HTTP request to Twitch."""
        response = self.http_session.request(
            method, urljoin(self.path, url.lstrip('/')), **kwargs)
        try:
            return response.json()
        except Exception:
            return response.text

    def connect(self, silent=False):
        """Connect to Twitch"""
        twitch_socket = websocket_connect(self.uri)
        twitch_socket.add_done_callback(self.authenticate)
        print(self.uri)

    def authenticate(self, future):
        """Auths with Twitch"""
        print("2")
        if future.exception() is None:
            self.websocket = future.result()
            self.websocket.write_message("PASS " + self.password)
            self.websocket.write_message("NICK " + self.username)
            self.websocket.write_message("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership")
            self.websocket.write_message("JOIN #" + self.channel)
            print("1")
            self.recv_message()
        else:
            raise ConnectionError(future.exception())

    @coroutine
    def recv_message(self, handler=None):
        """Read and handle messages from a Beam chat through a websocket."""

        while True:
            message = yield self.websocket.read_message()

            if message is None:
                self.logger.warning(
                    "Connection to chat server lost. Attempting to reconnect.")
                self.logger.debug("Connecting to: {server}.".format(
                    server=self.uri))

                authkey = self.get_chat(
                    self.connection_information["channel_id"])["authkey"]

                if self.connection_information["silent"]:
                    websocket_connection.add_done_callback(
                        partial(
                            self.authenticate,
                            self.connection_information["channel_id"]
                        )
                    )
                else:
                    websocket_connection.add_done_callback(
                        partial(
                            self.authenticate,
                            self.connection_information["channel_id"],
                            self.connection_information["bot_id"],
                            authkey
                        )
                    )

            response = loads(message)

            self.logger.debug("CHAT: {}".format(response))

            if callable(handler):
                handler(response)
            if message == "ping":
                self.send_message("PONG :tmi.twitch.tv")

    def send_message(self, message):
        self.twitchSocket.send("test")

Twitch().connect()

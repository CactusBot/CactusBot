import websocket
import socket

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
        websocket.enableTrace(True)

        with open('data/bots/bot.json', "r+") as config:
            bot = json.load(config)

        with open('data/config-template.json', "r+") as config:
            config = json.load(config)

        self.host = config["twitch"]["host"]
        self.port = config["twitch"]["port"]
        self.channel = bot["twitch"]["channel"]
        self.username = bot["twitch"]["username"]
        self.password = bot["twitch"]["password"]

        chat_socket = socket.socket()
        chat_socket.connect((self.host, self.port))
        chat_socket.send(bytes("PASS " + self.password), 'utf-8')
        chat_socket.send(bytes("NICK " + self.username), 'utf-8')
        chat_socket.send(bytes("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership"), 'utf-8')
        chat_socket.send(bytes("JOIN #" + self.channel), 'utf-8')

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

    def connect(self):
        self.uri = "ws://" + self.host + ":" + str(self.port)

        self.login_information = ['CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership', 'PASS ' + password, 'NICK ' + username, 'JOIN #' + channel]

        for login in login_information:
            self.twitchSocket.send(login)

    #@coroutine
    def recv_message(self):
        message = self.twitchSocket.recv()
        print(message)
        if message == "ping":
            self.send_message("PONG :tmi.twitch.tv")

    def send_message(self, message):
        self.twitchSocket.send("test")

Twitch().connect()

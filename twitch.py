from tornado.websocket import websocket_connect
from tornado.gen import coroutine
from tornado.ioloop import PeriodicCallback

from requests import Session
from requests.compat import urljoin

from logging import getLogger as get_logger
from logging import getLevelName as get_level_name
from logging import StreamHandler, FileHandler, Formatter

from functools import partial
from json import dumps, loads

from re import match

class Twitch():

    def __init__(self):
        self._init_logger(debug, kwargs.get("log_to_file", True))
        self.http_session = Session()

        with open('data/bots/bot.json', "r+") as config:
            data = json.load(config)

        self.host = data["twitch"]["host"]
        self.port = data["twitch"]["port"]
        self.channel = data["twitch"]["channel"]
        self.username = data["twitch"]["username"]
        self.password = data["twitch"]["password"]

        self.uri = "ws://" + self.host + ":" + self.port
        self.twitchSocket = websockets.client.connect(self.uri)

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

    def __exit__(self):
        self.twitchSocket.close()

    def conntect(self, username, password, channel):

        self.login_information = ['CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership', 'PASS ' + password, 'NICK ' + username, 'JOIN #' + channel]

        for login in login_information:
            self.twitchSocket.send(login)

    def recv_message(self):
        print(self.twitchSocket.recv())

    def send_message(self):
        self.twitchSocket.send("test")

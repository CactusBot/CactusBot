import socket

from requests import Session
from requests.compat import urljoin
import requests

from logging import getLogger as get_logger
from logging import getLevelName as get_level_name
from logging import StreamHandler, FileHandler, Formatter

from functools import partial
import json

from re import match

import time

class Twitch():

    def __init__(self, debug="INFO", **kwargs):
        self._init_logger(debug, kwargs.get("log_to_file", True))
        self.http_session = Session()

        # Change these to however you guys are storing data
        with open('data/bots/bot.json', "r+") as config:
            bot = json.load(config)

        with open('data/config-template.json', "r+") as config:
            config = json.load(config)

        # loads data
        self.host = config["twitch"]["host"]
        self.port = config["twitch"]["port"]
        self.channel = bot["twitch"]["channel"]
        self.username = bot["twitch"]["username"]
        self.password = bot["twitch"]["password"]

        # Creates socket. Leave this alone unless you know the socket module *cough* cubed *cough* not using websockets *cough*
        self.twitch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.twitch_socket.connect((self.host, self.port))

        self.authenticate()

    def _init_logger(self, level="INFO", file_logging=True, **kwargs):
        """Initialize logger. Copied from beam.py"""

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

    def authenticate(self):
        """Auths with Twitch"""
        self.twitch_socket.send(bytes("PASS " + self.password + "\n", "utf-8"))
        self.twitch_socket.send(bytes("NICK " + self.username + "\n", "utf-8"))
        self.twitch_socket.send(bytes("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership" + "\n", "utf-8"))
        self.twitch_socket.send(bytes("JOIN #" + self.channel + "\n", "utf-8"))

        self.twitch_login = requests.Session()
        self.twitch_login.post("https://api.twitch.tv/kraken?oauth_token={password}".format(password=self.password))
        #self.send_message("OHAI")
        #self.get_users()
        #self.get_followers()
        #self.set_game("Creative")
        #self.set_title("OHAI FROM CODE")

    def recv_message(self):
        """Recieves messages from Twitch IRC"""
        while True:
            readbuffer = b""
            readbuffer = readbuffer + self.twitch_socket.recv(1024)

            # Parses out the data recieved by splitting
            message_list = readbuffer.split(bytes("\n", "UTF-8"))
            parts = message_list[0].split(bytes(":", "UTF-8"))
            user = parts[1].split(bytes("!", "UTF-8"))
            message = parts[-1]

            # Twitch will sometimes do a keep alive PING. This should respond
            if "PING" in readbuffer:
                 self.twitch_socket.send(bytes("PONG :tmi.twitch.tv\r\n", "UTF-8"))

        return str(user), str(message)

    def send_message(self, message):
        """Use this to send a message, supports /commands"""
        self.twitch_socket.send(bytes("PRIVMSG #{channel} :".format(channel=self.channel) + message + "\n", "utf-8"))

    def get_users(self):
        """Gets all users in chat, no offical API so need to do this over IRC"""
        print(self.send_message("/NAMES #{channel}".format(channel=self.channel)))

    def get_followers(self):
        """Returns the latest follower"""
        pass
        #while True:
        #    follows = self.twitch_login.get("https://api.twitch.tv/kraken/channels/{channel}/follows".format(channel=self.channel))
        #    follow = follows.json()
        #    #print(follow)
        #    #newest = follow["created_at"]
        #    #second = follow["created_at"]
        #    if second == newest:
        #        return follow[0][user][display_name]
        #    time.sleep(.1)

    def get_hosts(self):
        pass

    def get_viewers(self):
        """Grabs all viewers in chat"""
        pass
        viewers = self.twitch_login.get("https://tmi.twitch.tv/group/user/{channel}/chatters".format(channel=self.channel))
        return str(viewers[chatters][viewers])

    def get_subs(self):
        """Gets the subs for a channel"""
        pass
        subs = self.twitch_login.get("https://api.twitch.tv/kraken/channels/{channel}/subscriptions".format(channel=self.channel))
        return str(subs["subscriptions"]["user"]["name"])

    def start_commercial(self, length):
        """Runs a commercial with the specified length"""
        self.send_message(bytes("PRIVMSG #{channel} : /comemrcial {length}\n".format(channel=self.channel, length=length), "UTF-8"))

    def set_title(self, title):
        """Sets the game on Twitch"""
        self.twitch_login.put("https://api.twitch.tv/kraken/channels/{channel}".format(channel=self.channel), data={"channel": {"status": title}})

    def set_game(self, game):
        """Sets the game on Twitch"""
        self.twitch_login.put("https://api.twitch.tv/kraken/channels/{channel}".format(channel=self.channel), data={"channel": {"game": game}})

Twitch()
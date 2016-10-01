"""Connects to Beam's chat and liveloading."""

from tornado.websocket import websocket_connect
from tornado.gen import coroutine

from requests import Session
from requests.compat import urljoin

from logging import getLogger as get_logger
from logging import getLevelName as get_level_name
from logging import StreamHandler, FileHandler, Formatter

from functools import partial
from json import dumps, loads

import re
import time

from models import User, session


class Beam:
    PATH = "https://beam.pro/api/v1/"

    def __init__(self, debug="INFO", **kwargs):
        self._init_logger(debug, kwargs.get("log_to_file", True))

        self.message_id = 0
        self.csrf_token = None
        self.quiet = None
        self.bot_id = None
        self.channel_id = None

        self.http_session = Session()

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
                "Module 'coloredlogs' unavailable; using normal logging.")

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

    def _init_users(self):
        viewers = set(
            user["userId"] for user in
            self.get_chat_users(self.channel_data["id"]))

        stored_users = set(
            user[0] for user in session.query(User).with_entities(User.id))

        for user in viewers - stored_users:
            user = User(id=user, joins=1)
            session.add(user)

        session.commit()

        self.logger.info("Successfully added new users to database.")

    def _request(self, url, method="GET", **kwargs):
        """Send HTTP request to Beam."""
        response = self.http_session.request(
            method,
            urljoin(self.PATH, url.lstrip('/')),
            headers={"X-CSRF-Token": self.csrf_token},
            **kwargs
        )

        if self.csrf_token is None:
            self.csrf_token = response.headers.get("X-CSRF-Token")
        elif response.status_code == 461:
            self.csrf_token = response.headers.get("X-CSRF-Token")
            self._request(url, method, **kwargs)

        try:
            return response.json()
        except Exception:
            return response.text

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        packet = {
            "username": username,
            "password": password,
            "code": code
        }
        return self._request("/users/login", method="POST", data=packet)

    def get_channel(self, id, **params):
        """Get channel data by username."""
        return self._request("/channels/{id}".format(id=id), params=params)

    def get_chat(self, id):
        """Get chat server data."""
        return self._request("/chats/{id}".format(id=id))

    def get_chat_users(self, id):
        return self._request("/chats/{id}/users".format(id=id))

    def connect(self, channel_id, bot_id, quiet=False):
        """Connect to a Beam chat through a websocket."""

        self.channel_id = channel_id
        self.bot_id = bot_id
        self.quiet = quiet

        self.connection_information = {
            "channel_id": self.channel_id,
            "bot_id": self.bot_id,
            "quiet": self.quiet
        }

        chat = self.get_chat(channel_id)

        self.servers = chat["endpoints"]
        self.server_offset = 0

        authkey = chat["authkey"]

        self.logger.debug("Connecting to: {server}.".format(
            server=self.servers[self.server_offset]))

        websocket_connection = websocket_connect(
            self.servers[self.server_offset])

        if quiet is True:
            websocket_connection.add_done_callback(
                partial(self.authenticate, channel_id))
        else:
            websocket_connection.add_done_callback(
                partial(self.authenticate, channel_id, bot_id, authkey))

    def authenticate(self, *args):
        """Authenticate session to a Beam chat through a websocket."""

        future = args[-1]
        if future.exception() is None:
            self.websocket = future.result()
            self.logger.info("Successfully connected to chat {}.".format(
                self.channel_data["token"]))

            self.send_message(*args[:-1], method="auth")

            if self.quiet:
                self.http_session = Session()

            self.read_chat(self.handle)
        else:
            self.logger.error("There was an issue connecting.")
            self.logger.error("Trying again in 10 seconds.")

            time.sleep(10)

            self.connect(self.channel_id, self.bot_id, self.quiet)

    def send_message(self, *args, method="msg"):
        """Send a message to a Beam chat through a websocket."""

        if self.quiet and method != "auth":
            if self.quiet is True:
                return

            if method == "msg":
                args = (self.quiet, r'\n'.join(args))
            elif method == "whisper":
                args = (
                    self.quiet,
                    "> {args[0]} | {args[1]}".format(
                        args=args,
                    )
                )
            method = "whisper"

        if method == "msg":
            for message in args:
                for chunk in re.findall(r'.{1,500}', message):
                    message_packet = {
                        "type": "method",
                        "method": "msg",
                        "arguments": (chunk,),
                        "id": self.message_id
                    }
                    self.websocket.write_message(dumps(message_packet))
                    self.message_id += 1

        else:
            message_packet = {
                "type": "method",
                "method": method,
                "arguments": args,
                "id": self.message_id
            }
            self.websocket.write_message(dumps(message_packet))
            self.message_id += 1

            if method == "whisper":
                self.logger.info("$ [{bot} > {user}] {message}".format(
                    bot=self.config["auth"]["username"],
                    user=args[0],
                    message=args[1]))

    def remove_message(self, message_id):
        """Remove a message from chat."""
        return self.send_message(message_id, method="deleteMessage")

    @coroutine
    def read_chat(self, handler=None):
        """Read and handle messages from a Beam chat through a websocket."""

        while True:
            message = yield self.websocket.read_message()

            if message is None:
                self.logger.warning(
                    "Connection to chat server lost. Attempting to reconnect.")

                self.server_offset += 1
                self.server_offset %= len(self.servers)

                self.logger.debug("Connecting to: {server}.".format(
                    server=self.servers[self.server_offset]))

                websocket_connection = websocket_connect(
                    self.servers[self.server_offset])

                try:
                    authkey = self.get_chat(
                        self.connection_information["channel_id"])["authkey"]
                except TypeError:
                    self.logger.error("Couldn't get the auth key from data.")
                    self.read_chat(self.handle)
                else:
                    if self.connection_information["quiet"]:
                        return websocket_connection.add_done_callback(
                            partial(
                                self.authenticate,
                                self.connection_information["channel_id"]
                            )
                        )
                    else:
                        return websocket_connection.add_done_callback(
                            partial(
                                self.authenticate,
                                self.connection_information["channel_id"],
                                self.connection_information["bot_id"],
                                authkey
                            )
                        )

            else:
                response = loads(message)

                self.logger.debug("CHAT: {}".format(response))

                if callable(handler):
                    handler(response)

    def connect_to_constellation(self, channel_id, user_id):
        """Connect to Beam liveloading."""

        self.constellation_connection_information = {
            "channel_id": channel_id,
            "user_id": user_id
        }

        constellation_websocket_connection = websocket_connect(
            "wss://constellation.beam.pro")
        constellation_websocket_connection.add_done_callback(
            partial(self.subscribe_to_liveloading, channel_id, user_id))

    def subscribe_to_liveloading(self, channel_id, user_id, future):
        """Subscribe to Beam constellation."""

        if future.exception() is None:
            self.constellation_websocket = future.result()

            self.logger.info(
                "Successfully connected to constellation websocket.")

            interfaces = [
                "channel:{channel}:update".format(channel=channel_id),
                "channel:{channel}:followed".format(channel=channel_id),
                "channel:{channel}:subscribed".format(channel=channel_id),
                "channel:{channel}:resubscribed".format(channel=channel_id),
                "channel:{channel}:hosted".format(channel=channel_id),
                "user:{user}:update".format(user=user_id)
            ]
            self.subscribe_to_interfaces(interfaces)

            self.logger.info(
                "Successfully subscribed to Constellation interfaces.")

            self.watch_constellation()
        else:
            self.logger.warning(future.exception())
            self.connect_to_constellation(channel_id, user_id)

    def subscribe_to_interfaces(self, interfaces: list):
        """Subscribe to a Beam constellation interface."""

        packet = {
            "type": "method",
            "method": "livesubscribe",
            "params": {
                "events": interfaces
            },
            "id": 1
        }
        self.constellation_websocket.write_message(dumps(packet))

    def parse_constellation_message(self, packet):
        try:
            packet = loads(packet)
        except:
            return ""
        else:
            if "data" in packet and "payload" in packet["data"]:
                return packet["data"]
            else:
                return ""

    @coroutine
    def watch_constellation(self):
        """Watch and handle packets from the Beam liveloading websocket."""

        response = yield self.constellation_websocket.read_message()
        if response is None:
            raise ConnectionError

        while True:
            message = yield self.constellation_websocket.read_message()
            message = self.parse_constellation_message(message)
            if message is None or message is "":
                pass
            else:
                self.logger.debug("LIVE: {}".format(message))
                if "followed" in message["channel"]:
                    if message["payload"]["following"]:
                        self.send_message(
                            "Thanks for the follow, @{} !".format(
                            message["payload"]["user"]["username"]))
                        self.logger.info("- {} followed.".format(
                            message["payload"]["user"]["username"]))
                elif "subscribed" in message["channel"]:
                    self.send_message("Thanks for subscribing, @{} !".format(
                        message["payload"]["user"]["username"]
                    ))
                elif "resubscribed" in message["channel"]:
                    self.send_message("Thanks for subscribing, @{} !".format(
                        message["payload"]["user"]["username"]
                    ))

            # if message is None:
            #     self.logger.info("Connection to Constellation lost.")
            #     self.logger.info("Attempting to reconnect.")

            #     return self.connect_to_constellation(
            #         **self.constellation_connection_information)

            #     self.logger.info("Attempting to reconnect.")
            #     self.watch_constellation()

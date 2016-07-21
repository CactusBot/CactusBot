"""Connects to Beam's chat and liveloading."""

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

import re
import time

from models import User, session
from datetime import datetime


class Beam:
    path = "https://beam.pro/api/v1/"

    message_id = 0

    def __init__(self, debug="INFO", **kwargs):
        self._init_logger(debug, kwargs.get("log_to_file", True))
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
            method, urljoin(self.path, url.lstrip('/')), **kwargs)
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

        self.connection_information = {
            "channel_id": channel_id,
            "bot_id": bot_id,
            "quiet": quiet
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

        backoff = 0

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
            self.logger.error("Trying again in {} seconds.".format(backoff))

            time.sleep(min(2**backoff, 60))
            backoff += 1

            self.authenticate(*args)

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

    def remove_message(self, channel_id, message_id):
        """Remove a message from chat."""
        return self._request("/chats/{id}/message/{message}".format(
            id=channel_id, message=message_id), method="DELETE")

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

    def connect_to_liveloading(self, channel_id, user_id):
        """Connect to Beam liveloading."""

        self.liveloading_connection_information = {
            "channel_id": channel_id,
            "user_id": user_id
        }

        liveloading_websocket_connection = websocket_connect(
            "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket")
        liveloading_websocket_connection.add_done_callback(
            partial(self.subscribe_to_liveloading, channel_id, user_id))

    def subscribe_to_liveloading(self, channel_id, user_id, future):
        """Subscribe to Beam liveloading."""

        if future.exception() is None:
            self.liveloading_websocket = future.result()

            self.logger.info(
                "Successfully connected to liveloading websocket.")

            interfaces = (
                "channel:{channel_id}:update",
                "channel:{channel_id}:followed",
                "channel:{channel_id}:subscribed",
                "channel:{channel_id}:resubscribed",
                "channel:{channel_id}:hosted",
                "user:{user_id}:update"
            )
            self.subscribe_to_interfaces(
                *tuple(
                    interface.format(channel_id=channel_id, user_id=user_id)
                    for interface in interfaces
                )
            )

            self.logger.info(
                "Successfully subscribed to liveloading interfaces.")

            self.watch_liveloading()
        else:
            self.logger.warning(future.exception())
            self.connect_to_liveloading(channel_id, user_id)

    def subscribe_to_interfaces(self, *interfaces):
        """Subscribe to a Beam liveloading interface."""

        packet = [
            "put",
            {
                "method": "put",
                "headers": {},
                "data": {
                    "slug": interfaces
                },
                "url": "/api/v1/live"
            }
        ]
        self.liveloading_websocket.write_message('420' + dumps(packet))

    def parse_liveloading_message(self, message):
        """Parse a message received from the Beam liveloading websocket."""

        sections = re.match(r"(\d+)(.+)?$", message).groups()

        return {
            "code": sections[0],
            "data": loads(sections[1]) if sections[1] is not None else None
        }

    @coroutine
    def watch_liveloading(self, handler=None):
        """Watch and handle packets from the Beam liveloading websocket."""

        response = yield self.liveloading_websocket.read_message()
        if response is None:
            raise ConnectionError

        packet = self.parse_liveloading_message(response)

        PeriodicCallback(
            partial(self.liveloading_websocket.write_message, '2'),
            packet["data"]["pingInterval"]
        ).start()

        while True:
            message = yield self.liveloading_websocket.read_message()

            if message is None:
                self.logger.info("Connection to Liveloading lost.")
                self.logger.info("Attempting to reconnect.")

                return self.connect_to_liveloading(
                    **self.liveloading_connection_information)

                self.logger.info("Attempting to reconnect.")
                self.watch_liveloading()

            packet = self.parse_liveloading_message(message)

            if packet.get("data") is not None:
                self.logger.debug("LIVE: {}".format(packet))

            if isinstance(packet["data"], list):
                if isinstance(packet["data"][0], str):
                    if packet["data"][1].get("following"):
                        self.logger.info("- {} followed.".format(
                            packet["data"][1]["user"]["username"]))

                        user = session.query(User).filter_by(
                            id=packet["data"][1]["user"]["id"]).first()
                        if user and (datetime.now() - user.follow_date).days:
                            self.send_message(
                                "Thanks for the follow, @{}!".format(
                                    packet["data"][1]["user"]["username"]))
                            user.follow_date = datetime.now()
                            session.add(user)
                            session.commit()
                    elif packet["data"][1].get("subscribed"):
                        self.logger.info("- {} subscribed.".format(
                            packet["data"][1]["user"]["username"]))
                        self.send_message(
                            "Thanks for the subscription, @{}! <3".format(
                                packet["data"][1]["user"]["username"]))
                    elif packet["data"][1].get("hoster"):
                        self.logger.info("- {} hosted the channel.".format(
                            packet["data"][1]["hoster"]["token"]))
                        self.send_message(
                            "Thanks for the hosting the channel, @{}!".format(
                                packet["data"][1]["hoster"]["token"]))

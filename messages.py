from beam import Beam
from models import (Command, User, session, CommandCommand, QuoteCommand,
                    CubeCommand, SocialCommand, UptimeCommand, PointsCommand,
                    TemmieCommand, FriendCommand, SpamProtCommand, ProCommand,
                    SubCommand, RepeatCommand)

from re import findall


class MessageHandler(Beam):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
        self.events = {
            "ChatMessage": self.message_handler,
            "UserJoin": self.join_handler,
            "UserLeave": self.leave_handler
        }

    def _init_commands(self):
        self.commands = {
            "cactus": "Ohai! I'm CactusBot. :cactus",
            "test": "Test confirmed. :cactus",
            "help": "Check out my documentation at cactusbot.readthedocs.org.",
            "command": CommandCommand(),
            "repeat": RepeatCommand(
                self.send_message,
                self.bot_data["username"],
                self.channel_data["token"]),
            "quote": QuoteCommand(),
            "social": SocialCommand(self.get_channel),
            "uptime": UptimeCommand(self._request),
            "friend": FriendCommand(self.get_channel),
            "points": PointsCommand(self.config["points"]["name"]),
            "spamprot": SpamProtCommand(self.update_config),
            "pro": ProCommand(),
            "sub": SubCommand(),
            "cube": CubeCommand(),
            "temmie": TemmieCommand()
        }

    def handle(self, response):
        if "event" in response:
            if response["event"] in self.events:
                self.events[response["event"]](response["data"])
            else:
                self.logger.debug("No handler found for event {}.".format(
                    response["event"]
                ))
        elif response.get("id") == 0:
            self.send_message("CactusBot activated. Enjoy! :cactus")

    def message_handler(self, data):
        parsed = str()
        for chunk in data["message"]["message"]:
            if chunk["type"] == "text":
                parsed += chunk["data"]
            else:
                parsed += chunk["text"]

        self.logger.info("{bot}{me}[{user}] {message}".format(
            bot='$ ' if data["user_name"] == self.config["auth"]["username"]
                else '',
            me='*' if data["message"]["meta"].get("me") else '',
            user=data["user_name"] + " > " + self.config["auth"]["username"]
                if data["message"]["meta"].get("whisper")
                else data["user_name"],
            message=parsed)
        )

        user = session.query(User).filter_by(id=data["user_id"]).first()
        if user is not None:
            user.messages += 1
            session.commit()
        else:
            user = User(id=data["user_id"], joins=1, messages=1)
            session.add(user)
            session.commit()

        mod_roles = ("Owner", "Staff", "Founder", "Global Mod", "Mod")
        if not (data["user_roles"][0] in mod_roles or user.friend):
            if (len(parsed) > self.config["spam_protection"].get(
                    "maximum_message_length", 256)):
                self.remove_message(data["channel"], data["id"])
                user.offenses += 1
                session.commit()
                return self.send_message(
                    data["user_name"], "Please stop spamming.",
                    method="whisper")
            elif (sum(char.isupper() for char in parsed) >
                    self.config["spam_protection"].get(
                        "maximum_message_capitals", 32)):
                self.remove_message(data["channel"], data["id"])
                user.offenses += 1
                session.commit()
                return self.send_message(
                    data["user_name"], "Please stop speaking in all caps.",
                    method="whisper")
            elif (sum(chunk["type"] == "emoticon"
                      for chunk in data["message"]["message"]) >
                    self.config["spam_protection"].get(
                    "maximum_message_emotes", 8)):
                self.remove_message(data["channel"], data["id"])
                user.offenses += 1
                session.commit()
                return self.send_message(
                    data["user_name"], "Please stop spamming emoticons.",
                    method="whisper")
            elif (findall(("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
                           "[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"),
                          parsed) and not
                    self.config["spam_protection"].get(
                        "allow_links", False)):
                self.remove_message(data["channel"], data["id"])
                user.offenses += 1
                session.commit()
                return self.send_message(
                    data["user_name"], "Please stop posting links.",
                    method="whisper")

        if parsed[0].startswith("!") and len(parsed) > 1:
            args = parsed.split()

            if args[0][1:] in self.commands:
                response = self.commands[args[0][1:]]
                if isinstance(response, str):
                    message = response
                else:
                    message = response(args, data)
            else:
                options = [
                    ('-'.join(args[:2])[1:], ['-'.join(args[:2])] + args[2:]),
                    (args[0][1:], args)
                ]

                for parse_method in options:
                    command = session.query(
                        Command).filter_by(command=parse_method[0]).first()
                    if command:
                        message = command(
                            parse_method[1], data,
                            channel_name=self.channel_data["token"]
                        )
                        break
                else:
                    message = "Command not found."

            if data["message"]["meta"].get("whisper", False):
                return self.send_message(
                    data["user_name"], message, method="whisper")
            else:
                return self.send_message(message)

    def join_handler(self, data):
        user = session.query(User).filter_by(id=data["id"]).first()
        if not user:
            user = User(id=data["id"], joins=1)
        else:
            session.add(user)
            user.joins += 1
        session.commit()

        self.logger.info("- {user} joined".format(
            user=data["username"]))

        if self.config.get("announce_enter", False):
            self.send_message("Welcome, @{username}!".format(
                username=data["username"]))

    def leave_handler(self, data):
        if data["username"] is not None:
            self.logger.info("- {user} left".format(
                user=data["username"]))

            if self.config.get("announce_leave", False):
                self.send_message("See you, @{username}!".format(
                    username=data["username"]))

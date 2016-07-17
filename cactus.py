# CactusBot!

from messages import MessageHandler
from beam import Beam

from models import Base, engine

from json import load, dump

from os.path import exists
from shutil import copyfile

from functools import reduce, partial

from tornado.ioloop import IOLoop
from tornado.autoreload import add_reload_hook, watch, start

from traceback import format_exc
from time import sleep

from argparse import ArgumentParser


cactus_art = r"""CactusBot initialized!

      ,`""',
      ;' ` ;
      ;`,',;
      ;' ` ;
 ,,,  ;`,',;               _____           _
;,` ; ;' ` ;   ,',        / ____|         | |
;`,'; ;`,',;  ;,' ;      | |     __ _  ___| |_ _   _ ___
;',`; ;` ' ; ;`'`';      | |    / _` |/ __| __| | | / __|
;` '',''` `,',`',;       | |___| (_| | (__| |_| |_| \__ \
 `''`'; ', ;`'`'          \_____\__,_|\___|\__|\__,_|___/
      ;' `';
      ;` ' ;
      ;' `';
      ;` ' ;
      ; ',';
      ;,' ';

Made by: 2Cubed, Innectic, and ParadigmShift3d
"""


class Cactus(MessageHandler, Beam):
    started = False
    connected = False

    def __init__(self, **kwargs):
        super(Cactus, self).__init__(**kwargs)

        self.debug = kwargs.get("debug", False)

        self.config_file = kwargs.get("config_file", "data/config.json")
        self.stats_file = kwargs.get("stats_file", "data/stats.json")
        self.database = kwargs.get("database", "data/data.db")

        self.quiet = kwargs.get("quiet", False)
        self.no_messages = kwargs.get("no_messages", False)

    def _init_database(self, database):
        """Ensure the database exists."""

        if exists(database):
            self.logger.info("Found database.")
        else:
            self.logger.info("Database wasn't found.")
            self.logger.info("Creating and setting defaults...")

            Base.metadata.create_all(engine)

            self.logger.info("Done!")

    def load_config(self, filename):
        """Load configuration file."""

        if exists(filename):
            self.logger.info("Configuration file found. Loading...")
            self.config_file = filename
            with open(filename) as config:
                self.config = load(config)
                return self.config
        else:
            self.logger.warn("Configuration file was not found. Creating...")
            copyfile("data/config-template.json", filename)
            self.logger.error(
                "Configuration file created. Please enter values and restart.")
            raise FileNotFoundError("Configuration file not found.")
            exit()

    def load_stats(self, filename):
        """Load statistics file."""

        self.logger.warning("Statistics are not yet implemented.")
        return dict()

        if exists(filename):
            self.stats_file = filename
            self.logger.info("Statistics file found. Loading...")
            with open(filename) as stats:
                self.stats = load(stats)
                return self.stats
        else:
            self.logger.warn("Statistics file not found. Creating...")
            copyfile("data/stats-template.json", "data/stats.json")
            self.logger.info("Statistics file created.")

    def update_config(self, keys, value):
        """Update configuration file value."""

        with open(self.config_file, 'r') as config:
            config_data = load(config)
            reduce(lambda d, k: d[k], keys.split('.')[:-1], config_data)[
                keys.split('.')[-1]] = value
        with open(self.config_file, 'w+') as config:
            dump(config_data, config, indent=2, sort_keys=True)
        self.config = config_data
        return self.config

    def update_stats(self, keys, value):
        """Update statistics file value."""

        self.logger.warning("Statistics are not yet implemented.")
        return

        with open(self.stats_file, 'r') as stats:
            stats_data = load(stats)
            reduce(lambda d, k: d[k], keys.split('.')[:-1], stats_data)[
                keys.split('.')[-1]] = value
        with open(self.stats_file, 'w+') as stats:
            dump(stats_data, stats, indent=2, sort_keys=True)
        self.stats = stats_data
        return self.stats

    def run(self, *args, **kwargs):
        """Run bot."""

        self.logger.info(cactus_art)
        self._init_database(self.database)
        self.load_config(filename=self.config_file)
        self.load_stats(filename=self.stats_file)
        self.started = True

        while self.config.get("autorestart") or not self.started:
            try:
                self.bot_data = self.login(**self.config["auth"])
                self.logger.info("Authenticated as: {}.".format(
                    self.bot_data["username"]))

                self.channel = self.config["channel"]
                self.channel_data = self.get_channel(self.channel)

                self._init_commands()
                self._init_users()

                self.connect(
                    self.channel_data["id"],
                    self.bot_data["id"],
                    quiet=self.quiet)

                def connect_liveloading():
                    try:
                        self.connect_to_liveloading(
                            self.channel_data["id"],
                            self.channel_data["userId"])
                    except ConnectionError as e:
                        self.logger.warning("Caught ConnectionError!")
                        self.logger.warning("Reconnecting to liveloading")
                        self.logger.warning(e)
                        connect_liveloading()

                connect_liveloading()

                if str(self.debug).lower() in ("true", "debug"):
                    add_reload_hook(partial(
                        self.send_message,
                        "Restarting, thanks to debug mode. :spaceship"
                    ))
                    watch(self.config_file)
                    start(check_time=5000)

                IOLoop.instance().start()

            except KeyboardInterrupt:
                print()
                self.logger.info("Removing thorns... done.")
                try:
                    self.send_message("CactusBot deactivated! :cactus")
                except Exception:
                    pass
                finally:
                    exit()

            except Exception:
                self.logger.critical("Oh no, I crashed!")

                try:
                    self.send_message("Oh no, I crashed! :127")
                except Exception:
                    pass

                self.logger.error('\n\n' + format_exc())

                if self.config.get("autorestart"):
                    self.logger.info("Restarting in 10 seconds...")
                    try:
                        sleep(10)
                    except KeyboardInterrupt:
                        self.logger.info("CactusBot deactivated.")
                        exit()
                else:
                    self.logger.info("CactusBot deactivated.")
                    exit()

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "--quiet",
        help="send no messages to public chat",
        metavar="USER",
        nargs='?',
        const=True,
        default=False
    )

    parser.add_argument(
        "--debug",
        help="set custom logger level",
        metavar="LEVEL",
        nargs='?',
        const=True,
        default="info"
    )

    parsed = parser.parse_args()

    cactus = Cactus(**parsed.__dict__)
    cactus.run()

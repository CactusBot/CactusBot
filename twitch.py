import json, string, time
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class Twitch():

    def __init__(self):
        with open('data/config-template.json', "r+") as config:    
            data = json.load(config)

        self.host = data["twitch"]["host"]
        self.port = data["twitch"]["port"]
        self.channel = data["twitch"]["channel"]
        self.username = data["twitch"]["username"]
        self.password = data["twitch"]["password"]

    def __exit__(self):
        pass
 
    

print(Twitch().recieve_message())
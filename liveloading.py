from websockets import connect
from json import loads, dumps
from re import match
from asyncio import get_event_loop, gather
from time import time
from threading import Thread
from statistics import Statistics
from user import User
from messages import MessageHandler as mh


class Liveloading:
    last_ping = 0

    follows = 0
    unfollows = 0
    subs = 0
    resubs = 0

    view_index = 0
    viewers = 0

    def connect(self, username):
        print("Connecting to the live-socket")

        self.websocket = yield from connect(
            "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket")
        response = yield from self.websocket.recv()
        self.interval = int(loads(self.parse_packet(response))["pingInterval"])
        self.last_ping = time()
        print("Connected to the live-socket")

        packet_template = [
            "put",
            {
                "method": "put",
                "headers": {},
                "data": {
                    "slug": [
                        "channel:2151:update"
                    ]
                },
                "url": "/api/v1/live"
            }
        ]

        assert response.startswith("0")

        events = (
            "channel:2151:update",
            "user:2547:update",
            "channel:2151:followed"
        )

        for event in events:
            packet = packet_template.copy()
            packet[1]["data"]["slug"][0] = event
            yield from self.websocket.send("420" + dumps(packet))

        response = yield from self.websocket.recv()
        print(response)

        assert response.startswith("40")
        yield from self.websocket.send("2")
        response = yield from self.websocket.recv()
        print(response, "RESP")

        assert response.startswith("42")
        print("Connected to the live-socket")

        yield from self.websocket.send("42")
        print("WASD", (yield from self.websocket.recv()))

        def ping_again():
            while True:
                if time() - self.last_ping > self.interval/1000:
                    self.last_ping = time()
                    self.websocket.send("2")
                    print(self.websocket.recv())
                    print("Reconnecting")
                Thread(target=ping_again).start()
        try:
            while True:
                response = yield from self.websocket.recv()
                print(response, "RESPONSE")
                packet = match('\d+(.+)?', response)
                if packet:
                    self.websocket.send("2")
                    if packet.group(1):
                        packet = loads(packet.group(1))
                        if isinstance(packet[0], str):
                            if packet[1].get("viewersCurrent"):
                                print("Viewer count is now {}.".format(
                                    packet[1].get("viewersCurrent")))
                            elif packet[1].get("numFollowers"):
                                print("Follower count is now {}.".format(
                                    packet[1].get("viewersCurrent")))
                                print(packet[1])
        except:
            if self.view_index is 0:
                print("Not enough samples!")
            else:
                average = self.viewers / self.view_index

            data = {
                "location": "live",

                "Subs": self.subs,
                "Resubs": self.resubs,
                "Follows": self.followers,
                "Unfollows": self.unfollowers,
                "AverageViewers": average
            }

            Statistics.recv(data)
            Statistics.recv(mh.get_data())

    def parse_packet(self, packet):
        return match('\d+(.+)?', packet).group(1)

server = Liveloading()
loop = get_event_loop()
loop.run_until_complete(gather(server.connect("misterjoker")))
# server.connect('2Cubed')

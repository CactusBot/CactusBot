# class StreamCommand(Command):
#
#     def __init__(self, request):
#         super(StreamCommand, self).__init__()
#         self.request = request
#
#     @mod_only
#     def __call__(self, args, data):
#         if len(args) >= 2:  # Want to confirm we're getting arg + contents
#             # Title or game
#             to_send = " ".join(args[2:])
#             if args[1] == "title":      # Set the stream title
#                 ret = self.request(url="/channels/" + str(data["channel"]),
#                                    method="PUT",
#                                    data={
#                                        "name": to_send
#                 })
#
#             elif args[1] == "game":     # Set the stream game
#                 ret = self.request(url="/channels/" + str(data["channel"]),
#                                    method="PUT",
#                                    data={
#                                        "typeId": to_send
#                 })
#
#                 if ret["type"]["name"] != to_send:
#                     return ret["details"]
#
#             else:
#                 return "Invalid argument: {}".format(args[1])
#
#             if ret["name"] != to_send:
#                 # Uh oh, it's not working :(
#                 return ret["details"][0]["message"]
#             else:
#                 return "Stream {} successfully set!".format(args[1])
#         else:
#             return "Not enough arguments!"

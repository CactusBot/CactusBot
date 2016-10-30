"""
The MIT License

Copyright (c) 2016 CactusDev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

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

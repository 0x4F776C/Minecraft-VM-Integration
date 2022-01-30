import asyncio
from socket import socket
import websockets
import json
from uuid import uuid4
import subprocess
import datetime
from sys import platform

async def running_ws(websocket, path):
    print("Running_WS - Connected")
    await websocket.send(
        json.dumps({
            "header": {
                "version": 1,
                "requestId": str(uuid4()),
                "messageType": "commandRequest",
                "messagePurpose": "subscribe"
            },
            "body": {
                "eventName": "PlayerMessage"
            },
        }))
    try:
        async for msg in websocket:
            msg = json.loads(msg)
            try:
                if msg["body"]["properties"]["Message"]:
                    print(f"<{msg['body']['properties']['Sender']}> {msg['body']['properties']['Message']}")
                    if msg["body"]["properties"]["Message"].startswith("!exec"):
                        
                        """
                        await websocket.send(
                            json.dumps({
                                "body": {
                                    "origin": {
                                        "type": "player"
                                    },
                                    "commandLine": msg["body"]["properties"]["Message"][6:],
                                    "version": 1
                                },
                                "header": {
                                    "requestId": str(uuid4()),
                                    "messagePurpose": "commandRequest",
                                    "version": 1,
                                    "messageType": "commandRequest"
                                }
                            }))
                        """

                        if platform == "linux" or platform == "linux2":
                            pipe = subprocess.Popen(f"/usr/bin/echo {msg['body']['properties']['Message'][6:]}", shell=True, stdout=subprocess.PIPE)
                            execution = subprocess.Popen("/usr/bin/sh", shell=True, stdin=pipe.stdout)
                        elif platform == "win32":
                            print(f"{platform} is not supported as of {datetime.datetime.now()}")
            except KeyError:
                pass
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")

#print("Type in: /connect 192.168.1.97:7000")
print(f"Program started at {datetime.datetime.now()}")

asyncio.get_event_loop().run_until_complete(websockets.serve(running_ws, host="192.168.1.97", port=7000))
asyncio.get_event_loop().run_forever()

"""
{ "body" : { "eventName" : "PlayerMessage" , "properties" : { "Message" : "!exec whoami" , "MessageType" : "chat" , "Sender" : "ChunHaoxx" } } }
"""
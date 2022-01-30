import asyncio
from socket import socket
import websockets
import json
from uuid import uuid4
import datetime
import requests

def send(cmd):
    msg = requests.post("ws://192.168.1.97:7000", json= {
        "header": {
            "version": 1,
            "requestId": str(uuid4()),
            "messageType": "commandRequest",
            "messagePurpose": "subscribe"
        },
        "body": {
            "version": 1,
            "commandLine": cmd,
            "origin": {
                "type": "player"
            }
        }
    })
    print(f"Status Code: {msg.status_code}, Response: {msg.json()}")

async def running_returning_ws(websocket, path):
    print("Running_Returning_WS - Connected")
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
                    if msg["body"]["properties"]["Message"].startswith("?exec"):
                        send(msg['body']['properties']['Message'][6:])
            except KeyError:
                pass
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")

#print("Type in: /connect 192.168.1.97:7000")
print(f"Program started at {datetime.datetime.now()}")

asyncio.get_event_loop().run_until_complete(websockets.serve(running_returning_ws, host="192.168.1.97", port=8000))
asyncio.get_event_loop().run_forever()

"""
{ "body" : { "eventName" : "PlayerMessage" , "properties" : { "Message" : "whoami" , "Sender" : "ChunHaoxx" } } }
"""
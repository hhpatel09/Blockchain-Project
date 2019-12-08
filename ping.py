#!/usr/bin/env python

# WS client example


import asyncio
import websockets
import json
import sys

apiMsgs = []
done = 0


async def PingApi(msgToSend):
    # uri = "ws://ws.dogechain.info/inv"
    uri = "wss://ws.blockchain.info/inv"
    async with websockets.connect(uri) as websocket:
        await websocket.send(msgToSend)
        while not done:
            result = await websocket.recv()
            # print(f"< {result}")
            apiMsgs.append(result)


async def getElementFromList():
    if apiMsgs:
        msg = apiMsgs[1]
        apiMsgs.remove(msg)


async def chain(msgToSend):
    apiMsgs = await PingApi(msgToSend)
    msg = await getElementFromList()
    print("hello")


assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
msgToSend = '{"op":"unconfirmed_sub"}'
asyncio.run(chain(msgToSend))
# returnMsg = asyncio.run(PingApi(msgToSend))
# for i in range(0, 10):
#     if apiMsgs:
#         msg = apiMsgs[1]
#         apiMsgs.remove(msg)
#         parsedMsg = json.loads(msg)
#         print(parsedMsg["msg"])

msgToSend = '{"op":"unconfirmed_unsub"}'
returnMsg = asyncio.run(PingApi(msgToSend))
done = 1

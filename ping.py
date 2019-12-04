#!/usr/bin/env python

# WS client example


import asyncio
import websockets
import json


async def pingApi():
    uri = "wss://ws.blockchain.info/inv"
    async with websockets.connect(uri) as websocket:
        msg = '{"op":"ping_block"}'
        await websocket.send(msg)

        result = await websocket.recv()
        # print(f"< {result}")
        return result

while True:
    returnMsg = asyncio.run(pingApi())
    parsedMsg = json.loads(returnMsg)
    print(parsedMsg["x"])

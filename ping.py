#!/usr/bin/env python

# WS client example

import asyncio
import websockets


async def hello():
    uri = "wss://ws.blockchain.info/inv"
    async with websockets.connect(uri) as websocket:
        # name = input("What's your name? ")
        msg = '{"op":"ping"}'
        await websocket.send(msg)

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
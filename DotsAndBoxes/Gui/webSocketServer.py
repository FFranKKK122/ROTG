import asyncio
import websockets
import json

connected = set()

async def click(websocket, path):
    connected.add(websocket)
    try:
        async for clickSide in websocket:
            #message is a dict
            message = json.loads(clickSide)
            await asyncio.wait([ws.send(json.dumps(message)) for ws in connected])
            print(clickSide)
    finally:
         connected.remove(websocket)

start_server = websockets.serve(click, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
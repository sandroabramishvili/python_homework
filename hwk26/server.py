import websockets, asyncio

client_list = {}

async def broadcast(username, message):
    
    for ws in client_list.values():
        await ws.send(f"{username}: {message}")

async def handler(websocket):
    
    username = await websocket.recv()
    client_list[username] = websocket
    try:
        async for message in websocket:
            print(f"{username}: {message}")
            await broadcast(username, message)
    finally:
        del client_list[username]

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started...")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
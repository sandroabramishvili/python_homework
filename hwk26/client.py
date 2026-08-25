import websockets, asyncio

async def receive_messages(websocket):
    async for message in websocket:
        print(f"\n{message}")

async def send_messages(websocket):
    while True:
        message = await asyncio.to_thread(input, "You: ")

        if message.lower() == "exit":
            print("Exiting...")
            break

        await websocket.send(message)

async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("Connected to the server. Type 'exit' to quit.")

        username = await asyncio.to_thread(input, "Choose a username: ")
        await websocket.send(username)

        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket))

        done, pending = await asyncio.wait(
            {receive_task, send_task}, return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
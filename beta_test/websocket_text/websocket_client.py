import asyncio
import websockets

async def hello():
    uri = "ws://localhost:5678"
    async with websockets.connect(uri) as websocket:
        #name = input("What's your name? ")

        #await websocket.send(name)
        #print(f">>> {name}")
        while True:
            greeting = await websocket.recv()
            print(f"<<< {greeting}")
            asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(hello())
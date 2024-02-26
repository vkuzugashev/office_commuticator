import asyncio
from flask import Flask
import requests, json
import websockets
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
async def hyloo(websocket):
    while True:
        msisdn = 'user2'
        response = requests.get(f'http://127.0.0.1:8000/clients/{msisdn}')
        content = response.content
        if response.status_code == 200:
            print(content)
            data = json.loads(content)
            print(data)
            message = data['client_id']
            await websocket.send(message)
            print('Success!')
        elif response.status_code == 404:
            print('Not Found.')
        await asyncio.sleep(random.random() * 2 + 1)

async def main():
    async with websockets.serve(hyloo, "localhost", 5678):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())

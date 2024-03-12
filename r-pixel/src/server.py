import asyncio
import csv
import json

import pandas as pd

from websockets.server import serve
import websockets

FILEPATH = './r-pixel/data/database.csv'
SERVER_IP = "0.0.0.0"
CLIENTS = set()


async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass


async def myBroadcast(message):
    print("broadcasting")
    print("broadcasted: ")
    print(message)

    m = json.loads(message)
    m_list = [m['data']]
    websockets.broadcast(CLIENTS, json.dumps([m_list[0]]))


async def notifyConnectedUsers(data):
    if CLIENTS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([
            asyncio.create_task(send(websocket, data))
            for websocket in CLIENTS
        ])


async def saveData(user_data):

    print("saving data")
    df = pd.DataFrame(user_data, index=[0])
    existing_df = pd.read_csv(FILEPATH)
    combined_df = pd.concat([existing_df, df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=['xCoord', 'yCoord'],
                                              keep='last')
    combined_df.to_csv(FILEPATH, header=True, index=False)


def getData():
    with open(FILEPATH, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]

    return data


async def onUserConnect(websocket):

    # problem with same user same browser reloading
    # page and multiple client connects
    CLIENTS.add(websocket)
    print(CLIENTS)

    try:
        async for message in websocket:
            m = json.loads(message)
            if m["cmd"] == 'pxl':
                m_list = [m['data']]
                await saveData(m_list[0])
                await myBroadcast(message=message)
            elif m["cmd"] == 'data':
                await websocket.send(json.dumps(getData()))
            else:
                await websocket.send("{message: 'returned nothing'}")
    finally:
        # this solves the multiple connect problem
        CLIENTS.remove(websocket)


async def main():
    async with serve(
        onUserConnect,
        SERVER_IP,
        8765,
        extra_headers=[
            ("Access-Control-Allow-Origin", "*"),
            ("Content-Security-Policy", "default-src 'self'"),
        ],
    ) as server:  # noqa f841
        await asyncio.Future()  # run forever


asyncio.run(main())

# 172.31.182.131:5500/r-pixel/app/template/

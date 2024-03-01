import asyncio
import csv

from websockets.server import serve

connected_users = {

}
# connection in dictionary speichern


async def notifyConnectedUsers():
    pass


async def saveData(data):
    with open('../data/database.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['time'],
                         data['xCoord'],
                         data['yCoord'],
                         data['color']])


async def onUserConnect(websocket):

    user_id = id(websocket)
    connected_users[user_id] = websocket

    try:
        async for message in websocket:

            if message[0] == 'pxl':
                websocket.send("came inside the if")
                saveData(message)

            await websocket.send("websocket.message")
    finally:
        del connected_users[user_id]

    print(connected_users)


async def main():
    async with serve(
        onUserConnect,
        "localhost",
        8765,
        extra_headers=[
            ("Access-Control-Allow-Origin", "*"),
            ("Content-Security-Policy", "default-src 'self'"),
        ],
    ) as server:  # noqa f841
        await asyncio.Future()  # run forever


asyncio.run(main())

# 172.31.180.245:5500/r-pixel/app/template/

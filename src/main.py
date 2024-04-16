import asyncio
import json
import time

import websockets
from PIL import Image


async def send_pixel_data():
    image = Image.open("picture.bmp")

    width, height = image.size

    uri = "ws://172.31.181.61:8765"
    async with websockets.connect(uri) as websocket:
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                packet = {
                    "cmd": "pxl",
                    "data": {
                        "timeMS": 0,
                        "xCoord": x * 10,
                        "yCoord": y * 10,
                        "color": "#{:02x}{:02x}{:02x}".format(
                            pixel[0], pixel[1], pixel[2]
                        ),
                    },
                }
                await websocket.send(json.dumps(packet))

                time.sleep(0.001)

                # response = await websocket.recv()
                # print(f"Received from server: {response}")

    image.close()


asyncio.get_event_loop().run_until_complete(send_pixel_data())

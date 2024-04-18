import json
import asyncio
import pytest
from websockets import ClientProtocol
import websockets
from unittest.mock import MagicMock
from websockets.sync.client import connect

from backend.server import myBroadcast, CLIENTS


VALID_FILEPATH = "r-pixel\\tests\\my_database.csv"


def example_data(x_val=10, y_val=20, color='#ffffff'):
    return {
        'cmd': 'pxl',
        'data':
        {
            'timeMS': 1713380797,
            'xCoord': x_val,
            'yCoord': y_val,
            'color': color,
        },
    }


def reset_csv():
    file = open(VALID_FILEPATH, "w")
    file.write("timeMS,xCoord,yCoord,color")
    file.close()


@pytest.mark.asyncio
async def test_onUserConnect():

    uri = "ws://localhost:8765"
    websocket = websockets.connect(uri)
    async with websockets.connect(uri) as websocket:
        # await onUserConnect(json.dumps(example_data()))
        assert websocket.is_client

        message_pxl = json.dumps(example_data())
        message_data = json.dumps({"cmd": "data"})
        message_invalid = json.dumps({"cmd": "invalid_cmd"})

        await websocket.send(message_pxl)
        result = await websocket.recv()
        assert result is not None

        await websocket.send(message_data)
        result = await websocket.recv()
        assert result is not None

        await websocket.send(message_invalid)
        result = await websocket.recv()
        assert result == "{message: 'returned nothing'}"


@pytest.mark.asyncio
async def test_myBroadcast():
    message = json.dumps(example_data())
    uri = "ws://localhost:8765"

    with connect(uri) as websocket1:
        with connect(uri) as websocket2:

            myBroadcast(message)

            await asyncio.sleep(0.1)
            websocket_result1 = websocket1.recv()
            assert websocket_result1 is not None
            assert websocket_result1 == "Received from backend: 'cmd': 'pxl', 'data': { 'timeMS': 1713380797, 'xCoord': x_val, 'yCoord': y_val, 'color': color, },"
            websocket_result2 = websocket2.recv()
            assert websocket_result2 is not None
            assert websocket_result2 == "Received from backend: 'cmd': 'pxl', 'data': { 'timeMS': 1713380797, 'xCoord': x_val, 'yCoord': y_val, 'color': color, },"


def test_connection():
    asyncio.run(connect_to_server())


@pytest.mark.asyncio
async def connect_to_server():

    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:

        message = json.dumps(example_data())
        # await websocket.send(message)

        response = await websocket.recv()
        assert True  # response is not None

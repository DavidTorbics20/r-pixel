import os
import pytest
from backend.server import saveData, getData

VALID_FILEPATH = "r-pixel\\tests\\my_database.csv"


def example_data(x_val, y_val, color='#ffffff'):
    return {
        'timeMS': 1713380797,
        'xCoord': x_val,
        'yCoord': y_val,
        'color': color
    }


def reset_csv():
    file = open(VALID_FILEPATH, "w")
    file.write("timeMS,xCoord,yCoord,color")
    file.close()


def test_checking_filepath():
    filepath = VALID_FILEPATH
    assert os.path.exists(filepath)


@pytest.mark.asyncio
async def test_non_existing_filepath():
    filepath = './non_existing_path/test_database.csv'
    with pytest.raises(Exception) as exception:
        test_data = example_data(10, 20)
        await saveData(user_data=test_data, filepath=filepath)
        assert "File not found" == exception.value


@pytest.mark.asyncio
async def test_adding_correct_data():

    initial_row_count = len(getData(filepath=VALID_FILEPATH))

    test_data = example_data(10, 20)
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)
    test_data = example_data(10, 30)
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)
    test_data = example_data(20, 30)
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)

    final_row_count = len(getData(filepath=VALID_FILEPATH))
    assert final_row_count == initial_row_count + 3
    reset_csv()


@pytest.mark.asyncio
async def test_duplicate_coordinates():
    initial_row_count = len(getData(filepath=VALID_FILEPATH))

    test_data = example_data(10, 20)
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)

    final_row_count = len(getData(filepath=VALID_FILEPATH))
    assert final_row_count == initial_row_count + 1
    reset_csv()


@pytest.mark.asyncio
async def test_duplicate_coordinates_color_check():
    color = '#123123'
    previous_color = '#000000'

    test_data = example_data(10, 20, previous_color)
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)
    test_data = example_data(10, 20, color=color)
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)

    last_row = getData(filepath=VALID_FILEPATH)

    assert last_row[0]['color'] != previous_color
    assert last_row[0]['color'] == color
    reset_csv()


@pytest.mark.asyncio
async def test_csv_x_time_missing():
    test_data = example_data(10, 20)
    del test_data['timeMS']
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)
    data = getData(filepath=VALID_FILEPATH)
    assert test_data not in data

    row_count = len(getData(filepath=VALID_FILEPATH))
    assert row_count == 0
    reset_csv()


@pytest.mark.asyncio
async def test_csv_x_coordinate_missing():
    test_data = example_data(10, 20)
    del test_data['xCoord']
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)
    data = getData(filepath=VALID_FILEPATH)
    assert test_data not in data

    row_count = len(getData(filepath=VALID_FILEPATH))
    assert row_count == 0
    reset_csv()


@pytest.mark.asyncio
async def test_csv_y_coordinate_missing():
    test_data = example_data(10, 20)
    del test_data['yCoord']
    await saveData(user_data=test_data, filepath=VALID_FILEPATH)
    data = getData(filepath=VALID_FILEPATH)
    assert test_data not in data

    row_count = len(getData(filepath=VALID_FILEPATH))
    assert row_count == 0
    reset_csv()


@pytest.mark.asyncio
async def test_csv_color_missing():
    test_data = example_data(10, 20)
    del test_data['color']
    await saveData(user_data=[test_data], filepath=VALID_FILEPATH)
    data = getData(filepath=VALID_FILEPATH)
    assert test_data not in data

    row_count = len(getData(filepath=VALID_FILEPATH))
    assert row_count == 0
    reset_csv()

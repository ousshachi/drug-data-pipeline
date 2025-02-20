import os
import json
import tempfile
import pytest
from src.data_load.load import save_to_json
from tests.config import FILE_OUTPUT_PATH ,INVALID_JSON

def test_save_to_json_creates_file():
    """Test that save_to_json creates a file and writes correct content."""
    data = {"key": "value"}
    
    # Call the function
    save_to_json(data, FILE_OUTPUT_PATH)

    # Assert that the file was created
    assert os.path.exists(FILE_OUTPUT_PATH)

    # Assert that the content matches
    with open(FILE_OUTPUT_PATH, 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
    assert loaded_data == data

    # Cleanup after test
    os.remove(FILE_OUTPUT_PATH)


def test_save_to_json_invalid_data():
    """Test that save_to_json raises an error for non-serializable data."""
    data = {"key": set([1, 2, 3])}  # Sets are not JSON serializable
   
    # Assert that a ValueError is raised
    with pytest.raises(ValueError):
        save_to_json(data, INVALID_JSON)

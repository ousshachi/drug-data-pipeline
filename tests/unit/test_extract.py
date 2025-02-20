import pytest
import pandas as pd
from unittest.mock import patch
from io import StringIO
import json

from src.data_extract.extract import load_csv, load_json


@patch("pandas.read_csv")
def test_load_csv_file_not_found(mock_read_csv):
    # Arrange: simulate FileNotFoundError
    mock_read_csv.side_effect = FileNotFoundError

    # Act: call the load_csv function
    result = load_csv("mock_file.csv")

    # Assert: check if None is returned
    assert result is None


@patch("pandas.read_csv")
def test_load_csv_empty_file(mock_read_csv):
    # Arrange: simulate EmptyDataError
    mock_read_csv.side_effect = pd.errors.EmptyDataError

    # Act: call the load_csv function
    result = load_csv("mock_empty_file.csv")

    # Assert: check if None is returned
    assert result is None


@patch("pandas.read_json")
def test_load_json_file_not_found(mock_read_json):
    # Arrange: simulate FileNotFoundError
    mock_read_json.side_effect = FileNotFoundError

    # Act: call the load_json function
    result = load_json("mock_file.json")

    # Assert: check if None is returned
    assert result is None


@patch("pandas.read_json")
def test_load_json_decode_error(mock_read_json):
    # Arrange: simulate JSONDecodeError
    mock_read_json.side_effect = json.JSONDecodeError("Expecting value", "", 0)

    # Act: call the load_json function
    result = load_json("mock_invalid_json.json")

    # Assert: check if None is returned
    assert result is None

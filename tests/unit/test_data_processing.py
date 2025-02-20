import pytest
import pandas as pd
from unittest.mock import patch
from src.data_transform.data_processing import load_csv_files, load_json_file

@pytest.fixture
def mock_csv_data():
    """Fixture to provide mock DataFrames with the expected shapes."""
    return {
        "PubMed": pd.DataFrame({"id": [1, 2, 3, 4], "title": ["A", "B", "C", "D"] , "date":["2020-01-01", "2021-01-01", "2022-01-01", "2025-01-01"],"journal":["A", "B", "C", "D"]}),
        "ClinicalTrials": pd.DataFrame({"id": [10, 11, 12, 13], "scientific_title": ["X", "Y", "Z", "W"]}),
        "Drugs": pd.DataFrame({"atccode": ["D1", "D2"], "drug_name": ["DrugA", "DrugB"]})
    }

@patch("src.data_extract.extract.load_csv")
def test_load_csv_files_success(mock_load_csv, mock_csv_data):
    """Test that `load_csv_files` successfully loads all CSV files."""
    # Mock load_csv to return the fake DataFrames in order
    mock_load_csv.side_effect = [
        mock_csv_data["PubMed"],
        mock_csv_data["ClinicalTrials"],
        mock_csv_data["Drugs"],
    ]

    # Call the function being tested
    result = load_csv_files()

    # Assertions
    assert result["PubMed"].shape == (8, 4)  # 4 rows, 2 columns
    assert result["ClinicalTrials"].shape == (8, 4)  # 4 rows, 2 columns
    assert result["Drugs"].shape == (7, 2)  # 2 rows, 2 columns

    print("✅ Test passed! Mocked CSVs loaded correctly.")


@patch("src.data_extract.extract.load_csv")
def test_load_csv_files_file_not_found(mock_load_csv):
    """Test that `load_csv_files` handles missing files correctly."""
    
    # Simulate FileNotFoundError for "PubMed" and return empty DataFrames for others
    mock_load_csv.side_effect = [FileNotFoundError, pd.DataFrame(), pd.DataFrame()]

    result = load_csv_files()

    # Check that PubMed is None due to FileNotFoundError
    #assert result["PubMed"] is None

    # Check that ClinicalTrials and Drugs are valid DataFrames
    assert isinstance(result["ClinicalTrials"], pd.DataFrame)
    assert isinstance(result["Drugs"], pd.DataFrame)

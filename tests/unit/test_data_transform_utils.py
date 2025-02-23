import pytest
import pandas as pd
from src.data_transform.utils.utils import (
    standardize_date_format,
    convert_id_to_string,
    sanitize_title_text,
    remove_rows_with_empty_titles_or_journals,
    remove_duplicate_ids_and_reindex,
)


# Test for standardize_date_format
def test_standardize_date_format():
    data = {"date_column": ["2021-12-01", "2022-01-15", "2025-02-19"]}
    df = pd.DataFrame(data)
    result_df = standardize_date_format(df, "date_column")

    # Test if the format is standardized
    assert result_df["date_column"][0] == "2021-12-01"
    assert result_df["date_column"][1] == "2022-01-15"
    assert result_df["date_column"][2] == "2025-02-19"


# Test for convert_id_to_string
def test_convert_id_to_string():
    data = {"id_column": [1, 2, 3]}
    df = pd.DataFrame(data)
    result_df = convert_id_to_string(df, "id_column")

    # Test if the ID column is converted to string
    assert isinstance(result_df["id_column"][0], str)
    assert result_df["id_column"][0] == "1"


# Test for sanitize_title_text
def test_sanitize_title_text():
    data = {"title_column": ["Title 1", "   Title 2 ", "Title 3"]}
    df = pd.DataFrame(data)
    result_df = sanitize_title_text(df, "title_column")

    # Test if the text is sanitized
    assert result_df["title_column"][0] == "Title 1"
    assert result_df["title_column"][1] == "Title 2"
    assert result_df["title_column"][2] == "Title 3"


# Test for remove_rows_with_empty_titles_or_journals
def test_remove_rows_with_empty_titles_or_journals():
    data = {
        "title_column": ["Title 1", None, "Title 3"],
        "journal_column": ["Journal A", "Journal B", None],
    }
    df = pd.DataFrame(data)
    result_df = remove_rows_with_empty_titles_or_journals(
        df, "title_column", "journal_column"
    )

    # Test if the rows with empty titles or journals are removed
    assert len(result_df) == 1  # Only one row should remain


# Test for remove_duplicate_ids_and_reindex
def test_remove_duplicate_ids_and_reindex():
    data = {"id_column": [1, 2, 2, 3, 4, 4]}
    df = pd.DataFrame(data)
    result_df = remove_duplicate_ids_and_reindex(df, "id_column")

    # Test if duplicates are removed and index is reset
    assert len(result_df) == 4  # Should only have 4 unique rows
    assert result_df["id_column"].iloc[0] == 1  # Check that the first id is 1
    assert result_df["id_column"].iloc[-1] == 4  # Check that the last id is 4


# Additional tests for error handling (optional)
def test_standardize_date_format_invalid_column():
    data = {"another_column": ["2021-12-01", "2022-01-15"]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        standardize_date_format(df, "non_existent_column")


def test_convert_id_to_string_invalid_column():
    data = {"another_column": [1, 2, 3]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        convert_id_to_string(df, "non_existent_column")

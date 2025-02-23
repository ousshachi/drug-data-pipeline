from unittest.mock import patch
import pandas as pd
from src.data_transform.data_cleaning import clean_data

# Sample DataFrames for testing
drugs_df = pd.DataFrame(
    {"atccode": ["A123", "B456", "C789"], "drug_name": ["Drug A", "Drug B", "Drug C"]}
)

pubmed_df = pd.DataFrame(
    {
        "id": [1, 2, 3],
        "date": ["2022-01-01", "2022-02-02", "2022-03-03"],
        "title": ["Title A", "Title B", "Title C"],
        "journal": ["Journal A", "Journal B", "Journal C"],
    }
)

clinical_trials_df = pd.DataFrame(
    {
        "id": [1, 2, 3],
        "date": ["2022-01-01", "2022-02-02", "2022-03-03"],
        "scientific_title": ["Title A", "Title B", "Title C"],
        "journal": ["Journal A", "Journal B", "Journal C"],
    }
)

dataframes_load_csv = {
    "Drugs": drugs_df,
    "PubMed": pubmed_df,
    "ClinicalTrials": clinical_trials_df,
}


# Mocking utils functions
@patch("src.data_transform.data_cleaning.utils.convert_id_to_string")
@patch("src.data_transform.data_cleaning.utils.remove_duplicate_ids_and_reindex")
@patch("src.data_transform.data_cleaning.utils.standardize_date_format")
@patch("src.data_transform.data_cleaning.utils.sanitize_title_text")
@patch(
    "src.data_transform.data_cleaning.utils.remove_rows_with_empty_titles_or_journals"
)
def test_clean_data(
    mock_remove_rows,
    mock_sanitize_title,
    mock_standardize_date,
    mock_remove_duplicates,
    mock_convert_id,
):
    # Arrange: mock the behavior of utils functions
    mock_convert_id.return_value = drugs_df
    mock_remove_duplicates.return_value = drugs_df
    mock_standardize_date.return_value = pubmed_df
    mock_sanitize_title.return_value = pubmed_df
    mock_remove_rows.return_value = pubmed_df

    # Act: call the clean_data function
    cleaned_data = clean_data(dataframes_load_csv)

    # Assert: Check the results
    assert "Drugs" in cleaned_data
    assert "PubMed" in cleaned_data
    assert "ClinicalTrials" in cleaned_data
    assert isinstance(cleaned_data["Drugs"], pd.DataFrame)
    assert isinstance(cleaned_data["PubMed"], pd.DataFrame)
    assert isinstance(cleaned_data["ClinicalTrials"], pd.DataFrame)

    # Verify utils functions were called
    mock_convert_id.assert_called_once()
    assert mock_remove_duplicates.call_count == 3
    mock_standardize_date.call_count == 2
    mock_sanitize_title.call_count == 2
    mock_remove_rows.call_count == 2

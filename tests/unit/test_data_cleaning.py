import sys
import os
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.data_transform.data_cleaning import clean_data, save_data_prepared
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))


# Sample DataFrames for testing
drugs_df = pd.DataFrame({
    'atccode': ['A123', 'B456', 'C789'],
    'drug_name': ['Drug A', 'Drug B', 'Drug C']
})

pubmed_df = pd.DataFrame({
    'id': [1, 2, 3],
    'date': ['2022-01-01', '2022-02-02', '2022-03-03'],
    'title': ['Title A', 'Title B', 'Title C'],
    'journal': ['Journal A', 'Journal B', 'Journal C']
})

clinical_trials_df = pd.DataFrame({
    'id': [1, 2, 3],
    'date': ['2022-01-01', '2022-02-02', '2022-03-03'],
    'scientific_title': ['Title A', 'Title B', 'Title C'],
    'journal': ['Journal A', 'Journal B', 'Journal C']
})

dataframes_load_csv = {
    'Drugs': drugs_df,
    'PubMed': pubmed_df,
    'ClinicalTrials': clinical_trials_df
}

# Mocking utils functions
@patch("src.data_transform.data_cleaning.utils.convert_id_to_string")
@patch("src.data_transform.data_cleaning.utils.remove_duplicate_ids_and_reindex")
@patch("src.data_transform.data_cleaning.utils.standardize_date_format")
@patch("src.data_transform.data_cleaning.utils.sanitize_title_text")
@patch("src.data_transform.data_cleaning.utils.remove_rows_with_empty_titles_or_journals")
def test_clean_data(mock_remove_rows, mock_sanitize_title, mock_standardize_date, mock_remove_duplicates, mock_convert_id):
    # Arrange: mock the behavior of utils functions
    mock_convert_id.return_value = drugs_df
    mock_remove_duplicates.return_value = drugs_df
    mock_standardize_date.return_value = pubmed_df
    mock_sanitize_title.return_value = pubmed_df
    mock_remove_rows.return_value = pubmed_df

    # Act: call the clean_data function
    cleaned_data = clean_data(dataframes_load_csv)

    # Assert: Check the results
    assert 'Drugs' in cleaned_data
    assert 'PubMed' in cleaned_data
    assert 'ClinicalTrials' in cleaned_data
    assert isinstance(cleaned_data['Drugs'], pd.DataFrame)
    assert isinstance(cleaned_data['PubMed'], pd.DataFrame)
    assert isinstance(cleaned_data['ClinicalTrials'], pd.DataFrame)

    # Verify utils functions were called
    mock_convert_id.assert_called_once()
    assert mock_remove_duplicates.call_count == 3 
    mock_standardize_date.call_count == 2 
    mock_sanitize_title.call_count == 2
    mock_remove_rows.call_count == 2


@patch("src.data_transform.data_cleaning.config")
@patch("src.data_transform.data_cleaning.pd.DataFrame.to_csv")
def test_save_data_prepared(mock_to_csv, mock_config):
    # Arrange: mock the config attributes
    mock_config.PUBMED_FILE_PREPARED = 'pubmed_prepared.csv'
    mock_config.CLINICAL_TRIALS_FILE_PREPARED = 'clinical_trials_prepared.csv'
    mock_config.DRUGS_FILE_PREPARED = 'drugs_prepared.csv'

    # Prepare a dictionary of cleaned data
    cleaned_data_df = {
        'PubMed': pubmed_df,
        'ClinicalTrials': clinical_trials_df,
        'Drugs': drugs_df
    }

    # Act: call the save_data_prepared function
    save_data_prepared(cleaned_data_df)

    # Assert: check that to_csv was called for each DataFrame
    mock_to_csv.assert_any_call('pubmed_prepared.csv', index=False)
    mock_to_csv.assert_any_call('clinical_trials_prepared.csv', index=False)
    mock_to_csv.assert_any_call('drugs_prepared.csv', index=False)

    # Assert the calls for specific files
    assert mock_to_csv.call_count == 3  # It should be called exactly 3 times


@patch("src.data_transform.data_cleaning.utils.convert_id_to_string")
@patch("src.data_transform.data_cleaning.utils.remove_duplicate_ids_and_reindex")
@patch("src.data_transform.data_cleaning.utils.standardize_date_format")
@patch("src.data_transform.data_cleaning.utils.sanitize_title_text")
@patch("src.data_transform.data_cleaning.utils.remove_rows_with_empty_titles_or_journals")
def test_clean_data_missing_key(mock_remove_rows, mock_sanitize_title, mock_standardize_date, mock_remove_duplicates, mock_convert_id):
    # Arrange: Prepare a dictionary with missing key 'Drugs'
    incomplete_dataframes = {
        'PubMed': pubmed_df,
        'ClinicalTrials': clinical_trials_df
    }

    # Act & Assert: Check if KeyError is raised due to missing required keys
    with pytest.raises(KeyError):
        clean_data(incomplete_dataframes)
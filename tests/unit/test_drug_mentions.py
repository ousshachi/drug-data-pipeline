import pytest
import pandas as pd
from src.data_transform.drug_mentions import find_mentions

@pytest.fixture
def mock_data():
    """Fixture to provide mock data for PubMed, ClinicalTrials, and Drugs DataFrames."""
    # PubMed mock data
    pubmed_data = {
        "title": ["Study on DrugA", "Research on DrugB", "DrugC effects"],
        "journal": ["Journal1", "Journal2", "Journal3"],
        "date": ["2020-01-01", "2020-02-01", "2020-03-01"]
    }
    pubmed_df = pd.DataFrame(pubmed_data)

    # Clinical Trials mock data
    clinical_trials_data = {
        "scientific_title": ["Trial involving DrugA", "DrugB clinical trial", "Effects of DrugC in patients"],
        "journal": ["CT Journal1", "CT Journal2", "CT Journal3"],
        "date": ["2020-01-15", "2020-02-15", "2020-03-15"]
    }
    clinical_trials_df = pd.DataFrame(clinical_trials_data)

    # Drugs mock data
    drugs_data = {"drug": ["DrugA", "DrugB", "DrugC"]}
    drugs_df = pd.DataFrame(drugs_data)

    return pubmed_df, clinical_trials_df, drugs_df

def test_find_mentions_success(mock_data):
    """Test that the function correctly identifies drug mentions in publications."""
    pubmed_df, clinical_trials_df, drugs_df = mock_data

    # Call the function
    mentions = find_mentions(pubmed_df, clinical_trials_df, drugs_df)

    # Assert that the function returns the correct number of mentions
    assert len(mentions) == 6  # 3 from PubMed and 3 from Clinical Trials

    # Check that the mentions contain the correct drug, source, title, journal, and date
    assert mentions[0]["drug"] == "DrugA"
    assert mentions[0]["source"] == "pubmed"
    assert mentions[0]["title"] == "Study on DrugA"
    assert mentions[0]["journal"] == "Journal1"
    assert mentions[0]["date"] == "2020-01-01"

    assert mentions[3]["drug"] == "DrugA"
    assert mentions[3]["source"] == "clinical_trials"
    assert mentions[3]["title"] == "Trial involving DrugA"
    assert mentions[3]["journal"] == "CT Journal1"
    assert mentions[3]["date"] == "2020-01-15"

def test_find_mentions_missing_drug_column(mock_data):
    """Test that the function raises an error if the drugs dataframe is missing the 'drug' column."""
    pubmed_df, clinical_trials_df, _ = mock_data

    # Create a drugs dataframe without the 'drug' column
    drugs_df_missing_column = pd.DataFrame({"other_column": ["DrugA", "DrugB", "DrugC"]})

    # Assert that the ValueError is raised
    with pytest.raises(ValueError, match="The drugs dataframe must have a 'drug' column."):
        find_mentions(pubmed_df, clinical_trials_df, drugs_df_missing_column)

def test_find_mentions_missing_title_column(mock_data):
    """Test that the function raises an error if the title column is missing in either PubMed or Clinical Trials."""
    pubmed_df, _, drugs_df = mock_data

    # Create PubMed dataframe missing the 'title' column
    pubmed_df_missing_title = pubmed_df.drop(columns=["title"])

    # Assert that the ValueError is raised
    with pytest.raises(ValueError, match="Missing required 'title' column in pubmed dataframe."):
        find_mentions(pubmed_df_missing_title, pubmed_df, drugs_df)

def test_find_mentions_empty_titles(mock_data):
    """Test that the function handles empty titles correctly."""
    _, clinical_trials_df, drugs_df = mock_data

    # Modify Clinical Trials to include empty titles
    clinical_trials_df_with_empty_titles = clinical_trials_df.copy()
    clinical_trials_df_with_empty_titles["scientific_title"] = ""

    # Call the function
    mentions = find_mentions(_, clinical_trials_df_with_empty_titles, drugs_df)

    # Assert no mentions should be found
    assert len(mentions) == 3

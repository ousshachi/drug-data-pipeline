import pandas as pd
from src.data_extract.extract import find_mentions, build_relationships

def test_find_mentions_in_clinical_trials():
    """Test finding mentions of drugs in clinical trials."""
    drugs_df = pd.DataFrame({"drug": ["DrugA", "DrugB"]})
    clinical_trials_df = pd.read_csv("tests/test_data/clinical_trials.csv")
    
    dataframes = {"clinical_trials": clinical_trials_df}
    
    mentions = find_mentions(dataframes, drugs_df)
    
    assert len(mentions) == 2  # Only DrugA and DrugB are mentioned
    assert mentions[0]["drug"] == "DrugA"
    assert mentions[1]["drug"] == "DrugB"

def test_build_relationships_from_clinical_trials():
    """Test building relationships from clinical trial mentions."""
    mentions = [
        {"drug": "DrugA", "source": "clinical_trials", "title": "Trial with DrugA",
         "journal": "JournalX", "date": "2025-01-01"},
        {"drug": "DrugB", "source": "clinical_trials", "title": "Another trial mentioning DrugB",
         "journal": "JournalY", "date": "2025-01-02"}
    ]
    
    relationships = build_relationships(mentions)
    
    assert len(relationships) == 2  # Two drugs have relationships
    assert relationships["DrugA"]["publications"][0]["journal"] == "JournalX"
    assert relationships["DrugB"]["publications"][0]["journal"] == "JournalY"

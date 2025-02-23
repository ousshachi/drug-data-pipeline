from src.data_transform.relationships import build_relationships


def test_build_relationships_from_clinical_trials():
    """Tester la construction de relations à partir des mentions dans les essais cliniques."""
    mentions = [
        {
            "drug": "DrugA",
            "source": "clinical_trials",
            "title": "Trial with DrugA",
            "journal": "JournalX",
            "date": "2025-01-01",
        },
        {
            "drug": "DrugB",
            "source": "clinical_trials",
            "title": "Another trial mentioning DrugB",
            "journal": "JournalY",
            "date": "2025-01-02",
        },
    ]

    relationships = build_relationships(mentions)

    assert len(relationships) == 2  # Deux médicaments ont des relations
    assert relationships["DrugA"]["publications"][0]["journal"] == "JournalX"
    assert relationships["DrugB"]["publications"][0]["journal"] == "JournalY"

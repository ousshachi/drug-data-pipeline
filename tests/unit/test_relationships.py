import pytest
from src.data_transform.relationships import build_relationships


@pytest.fixture
def mentions():
    return [
        {
            "drug": "aspirin",
            "source": "pubmed",
            "title": "Aspirin and its effects",
            "journal": "Nature",
            "date": "2023-01-01",
        },
        {
            "drug": "paracetamol",
            "source": "pubmed",
            "title": "Paracetamol usage in children",
            "journal": "Science",
            "date": "2023-02-15",
        },
    ]


def test_build_relationships(mentions):
    relationships = build_relationships(mentions)

    assert "aspirin" in relationships
    assert "paracetamol" in relationships
    assert len(relationships["aspirin"]["publications"]) == 1
    assert relationships["aspirin"]["publications"][0]["journal"] == "Nature"

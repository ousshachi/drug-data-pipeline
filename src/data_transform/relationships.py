import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def build_relationships(
    mentions: List[Dict[str, str]]
) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    """
    Build relationships between drugs and their mentions in publications.

    Args:
        mentions (List[Dict[str, str]]): A list of drug mention dictionaries.

    Returns:
        Dict[str, Dict[str, List[Dict[str, str]]]]: A dictionary mapping each drug to its publication mentions.

    Raises:
        ValueError: If the mentions list is empty or contains invalid entries.
    """

    if not mentions:
        logging.warning(
            "No mentions provided. Returning an empty relationships dictionary."
        )
        return {}

    relationships = {}

    # Process each mention and build relationships
    for mention in mentions:
        drug = mention.get("drug")
        if not isinstance(drug, str) or not drug.strip():
            logging.warning(f"Skipping invalid drug entry: {mention}")
            continue  # Skip invalid drug names

        publication_data = {
            "source": mention.get("source", ""),
            "title": mention.get("title", ""),
            "journal": mention.get("journal", ""),
            "date": mention.get("date", ""),
        }

        # Use setdefault to simplify dictionary structure creation
        relationships.setdefault(drug, {"publications": []})["publications"].append(
            publication_data
        )

    logging.info(f"Built relationships for {len(relationships)} unique drugs.")
    return relationships

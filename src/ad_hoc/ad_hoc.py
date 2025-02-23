import logging
import json
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_top_journal_by_unique_drugs(json_file: str) -> str:
    """
    Extract the journal that mentions the most unique drugs from the JSON file.

    Args:
        json_file (str): Path to the JSON file produced by the data pipeline.

    Returns:
        str: The name of the journal that mentions the most unique drugs.
    """
    try:
        # Load the JSON file
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Dictionary to count unique drugs per journal
        journal_drug_map = defaultdict(set)

        # Iterate through each drug and its publications
        for drug, details in data.items():
            for publication in details.get("publications", []):
                journal = publication.get("journal")
                if journal:
                    journal_drug_map[journal].add(drug)

        # Find the journal with the most unique drugs
        top_journal = max(journal_drug_map.items(), key=lambda x: len(x[1]))

        logging.info(
            f"The journal mentioning the most unique drugs is "
            f"'{top_journal[0]}' with {len(top_journal[1])} unique drugs."
        )

        return top_journal[0]

    except FileNotFoundError:
        logging.error(f"Error: The file {json_file} does not exist.")
    except json.JSONDecodeError as e:
        logging.error(f"Error: Failed to parse JSON file. Details: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

import pandas as pd
import re
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def find_mentions(pubmed_df: pd.DataFrame, clinical_trials_df: pd.DataFrame, drugs_df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Identify mentions of drugs in publications from PubMed and ClinicalTrials dataframes.

    Args:
        pubmed_df (pd.DataFrame): DataFrame containing PubMed data.
        clinical_trials_df (pd.DataFrame): DataFrame containing Clinical Trials data.
        drugs_df (pd.DataFrame): DataFrame containing drug names.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing drug mentions in publications.

    Raises:
        ValueError: If required columns are missing from any dataframe.
    """

    # Validate required columns
    if "drug" not in drugs_df.columns:
        raise ValueError("The drugs dataframe must have a 'drug' column.")

    data_sources = {
        "pubmed": {"df": pubmed_df, "title_col": "title"},
        "clinical_trials": {"df": clinical_trials_df, "title_col": "scientific_title"},
    }

    mentions = []
    drug_patterns = {drug: re.compile(rf"\b{re.escape(drug)}\b", re.IGNORECASE) for drug in drugs_df["drug"].dropna()}

    for source_name, source_data in data_sources.items():
        df, title_col = source_data["df"], source_data["title_col"]

        if title_col not in df.columns:
            raise ValueError(f"Missing required '{title_col}' column in {source_name} dataframe.")

        df = df.dropna(subset=[title_col])  # Remove rows with empty titles

        for drug, pattern in drug_patterns.items():
            matches = df[df[title_col].str.contains(pattern, regex=True, na=False)]
            for _, row in matches.iterrows():
                mentions.append({
                    "drug": drug,
                    "source": source_name,
                    "title": row[title_col],
                    "journal": row.get("journal", ""),
                    "date": row.get("date", "") if pd.notna(row.get("date")) else "",
                })

    logging.info(f"Found {len(mentions)} drug mentions in publications.")
    return mentions

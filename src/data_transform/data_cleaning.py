from .utils import utils
import logging
import pandas as pd
from typing import Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def clean_data(dataframes_load_csv: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Cleans and prepares the input dataframes by standardizing formats, removing duplicates,
    and handling missing values.

    Args:
        dataframes_load_csv (Dict[str, pd.DataFrame]): A dictionary containing raw dataframes with keys:
            - "Drugs": DataFrame containing drug data.
            - "PubMed": DataFrame containing PubMed data.
            - "ClinicalTrials": DataFrame containing Clinical Trials data.

    Returns:
        Dict[str, pd.DataFrame]: Dictionary containing cleaned dataframes with keys:
            - "PubMed"
            - "ClinicalTrials"
            - "Drugs"
    """

    required_keys = {"Drugs", "PubMed", "ClinicalTrials"}

    # Validate presence of required keys
    missing_keys = required_keys - dataframes_load_csv.keys()
    if missing_keys:
        raise KeyError(f"Missing required dataframes: {missing_keys}")

    # Log the start of the cleaning process
    logging.info("Starting data cleaning process...")

    try:
        # Clean and Prepare drugs_df
        logging.info("Cleaning Drugs dataframe...")
        drugs_df = utils.convert_id_to_string(dataframes_load_csv["Drugs"], "atccode")
        drugs_df = utils.remove_duplicate_ids_and_reindex(drugs_df, "atccode")

        # Clean and Prepare pubmed_df
        logging.info("Cleaning PubMed dataframe...")
        pubmed_df = utils.standardize_date_format(dataframes_load_csv["PubMed"], "date")
        pubmed_df = utils.sanitize_title_text(pubmed_df, "title")
        pubmed_df = utils.remove_rows_with_empty_titles_or_journals(
            pubmed_df, "title", "journal"
        )
        pubmed_df = utils.remove_duplicate_ids_and_reindex(pubmed_df, "id")

        # Clean and Prepare clinical_trials_df
        logging.info("Cleaning ClinicalTrials dataframe...")
        clinical_trials_df = utils.standardize_date_format(
            dataframes_load_csv["ClinicalTrials"], "date"
        )
        clinical_trials_df = utils.sanitize_title_text(
            clinical_trials_df, "scientific_title"
        )
        clinical_trials_df = utils.remove_rows_with_empty_titles_or_journals(
            clinical_trials_df, "scientific_title", "journal"
        )
        clinical_trials_df = utils.remove_duplicate_ids_and_reindex(
            clinical_trials_df, "id"
        )

        # Log completion
        logging.info("Data cleaning process completed successfully.")

        # Create and return a dictionary of cleaned DataFrames
        return {
            "PubMed": pubmed_df,
            "ClinicalTrials": clinical_trials_df,
            "Drugs": drugs_df,
        }

    except KeyError as e:
        logging.error(f"KeyError: {e}")
        raise

    except Exception as e:
        logging.error(f"An unexpected error occurred during data cleaning: {e}")
        raise

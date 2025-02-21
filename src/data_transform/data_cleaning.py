
from src import config
from .utils import utils
import logging
import pandas as pd
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
        pubmed_df = utils.remove_rows_with_empty_titles_or_journals(pubmed_df, "title", "journal")
        pubmed_df = utils.remove_duplicate_ids_and_reindex(pubmed_df, "id")

        # Clean and Prepare clinical_trials_df
        logging.info("Cleaning ClinicalTrials dataframe...")
        clinical_trials_df = utils.standardize_date_format(dataframes_load_csv["ClinicalTrials"], "date")
        clinical_trials_df = utils.sanitize_title_text(clinical_trials_df, "scientific_title")
        clinical_trials_df = utils.remove_rows_with_empty_titles_or_journals(clinical_trials_df, "scientific_title", "journal")
        clinical_trials_df = utils.remove_duplicate_ids_and_reindex(clinical_trials_df, "id")

        # Log completion
        logging.info("Data cleaning process completed successfully.")

        # Create and return a dictionary of cleaned DataFrames
        return {
            "PubMed": pubmed_df,
            "ClinicalTrials": clinical_trials_df,
            "Drugs": drugs_df
        }

    except KeyError as e:
        logging.error(f"KeyError: {e}")
        raise

    except Exception as e:
        logging.error(f"An unexpected error occurred during data cleaning: {e}")
        raise


def save_data_prepared(cleaned_data_df: Dict[str, pd.DataFrame]) -> None:
    """
    Save cleaned data into preparation files.

    Args:
        cleaned_data_df (Dict[str, pd.DataFrame]): A dictionary containing cleaned DataFrames.
            Expected keys:
                - "PubMed"
                - "ClinicalTrials"
                - "Drugs"
    
    Returns:
        None
    """
    
    required_keys = {"PubMed", "ClinicalTrials", "Drugs"}
    
    # Validate required keys
    missing_keys = required_keys - cleaned_data_df.keys()
    if missing_keys:
        raise KeyError(f"Missing required cleaned dataframes: {missing_keys}")

    # Validate config attributes
    required_config_attrs = {
        "PUBMED_FILE_PREPARED",
        "CLINICAL_TRIALS_FILE_PREPARED",
        "DRUGS_FILE_PREPARED"
    }
    
    missing_config_attrs = [attr for attr in required_config_attrs if not hasattr(config, attr)]
    if missing_config_attrs:
        raise AttributeError(f"Missing required config attributes: {missing_config_attrs}")

    try:
        # Save PubMed data
        logging.info(f"Saving PubMed data to {config.PUBMED_FILE_PREPARED}...")
        cleaned_data_df["PubMed"].to_csv(config.PUBMED_FILE_PREPARED, index=False)
        
        # Save ClinicalTrials data
        logging.info(f"Saving ClinicalTrials data to {config.CLINICAL_TRIALS_FILE_PREPARED}...")
        cleaned_data_df["ClinicalTrials"].to_csv(config.CLINICAL_TRIALS_FILE_PREPARED, index=False)
        
        # Save Drugs data
        logging.info(f"Saving Drugs data to {config.DRUGS_FILE_PREPARED}...")
        cleaned_data_df["Drugs"].to_csv(config.DRUGS_FILE_PREPARED, index=False)

        logging.info("All cleaned data files have been successfully saved.")

    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
        raise
    
    except PermissionError as e:
        logging.error(f"PermissionError: {e}")
        raise
    
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving data: {e}")
        raise
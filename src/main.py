import logging
from config import OUTPUT_JSON_PATH, AD_HOC_OUTPUT_PATH

from data_transform.data_processing import load_csv_files
from data_transform.drug_mentions import find_mentions
from data_transform.relationships import build_relationships
from data_transform.data_cleaning import clean_data
from ad_hoc.ad_hoc import get_top_journal_by_unique_drugs
from data_load.load import save_to_json

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_data():
    """Main pipeline function to process drug mentions in publications."""
    try:
        # Extract
        logging.info("=" * 50)
        logging.info("1- Loading CSV files...\n")

        loaded_dataframes = load_csv_files()

        # trasform
        logging.info("=" * 50)
        logging.info("2- Cleaning data...\n")

        cleaned_data_df = clean_data(loaded_dataframes)

        logging.info("=" * 50)
        logging.info("3- Finding drug mentions in publications...\n")

        mentions = find_mentions(
            cleaned_data_df["PubMed"],
            cleaned_data_df["ClinicalTrials"],
            cleaned_data_df["Drugs"],
        )

        logging.info("=" * 50)
        logging.info("4- Building relationships...\n")
        relationships = build_relationships(mentions)

        # load
        logging.info("=" * 50)
        logging.info(f"5- Saving final JSON output to {OUTPUT_JSON_PATH}...\n")
        save_to_json(relationships, OUTPUT_JSON_PATH)

        logging.info("✅ Data processing completed successfully.")

        logging.info("=" * 50)
        logging.info(f"6- Generating ad_hoc...{''}\n")

        dataframe_df = get_top_journal_by_unique_drugs(OUTPUT_JSON_PATH)

        logging.info("=" * 50)
        logging.info(f"7- Saving adoc file {AD_HOC_OUTPUT_PATH}...\n")
        save_to_json(dataframe_df, AD_HOC_OUTPUT_PATH)

        return relationships

    except Exception as e:
        logging.error(f"❌ An error occurred during data processing: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    process_data()

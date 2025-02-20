import logging
from data_transform.data_processing import load_csv_files
from data_transform.drug_mentions import find_mentions
from data_transform.relationships import build_relationships
from data_transform.data_cleaning import clean_data, save_data_prepared
from data_load.load import save_to_json
from src import config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def process_data():
    """Main pipeline function to process drug mentions in publications."""
    try:
        logging.info("=" * 50)
        logging.info("1- Loading CSV files...\n")
       
        loaded_dataframes = load_csv_files()

        logging.info("=" * 50)
        logging.info("2- Cleaning data...\n")
       
        cleaned_data_df = clean_data(loaded_dataframes)

        # Optional: Save cleaned data to CSV files
        logging.info("=" * 50)
        logging.info("3- Saving prepared files optinal step because...\n")
      
        save_data_prepared(cleaned_data_df)

        logging.info("=" * 50)
        logging.info("4- Finding drug mentions in publications...\n")
  
        mentions = find_mentions(
            cleaned_data_df["PubMed"], 
            cleaned_data_df["ClinicalTrials"], 
            cleaned_data_df["Drugs"]
        )
        
        logging.info("=" * 50)
        logging.info("5- Building relationships...\n")
        relationships = build_relationships(mentions)
    

        logging.info("=" * 50)
        logging.info(f"6- Saving final JSON output to {config.OUTPUT_JSON_PATH}...\n")
        save_to_json(relationships, config.OUTPUT_JSON_PATH)

        logging.info("✅ Data processing completed successfully.")
        return relationships

    except Exception as e:
        logging.error(f"❌ An error occurred during data processing: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    process_data()

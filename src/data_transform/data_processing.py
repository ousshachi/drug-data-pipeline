import logging
import pandas as pd
from src.data_extract.extract import load_csv
from src.config import DRUGS_FILE, PUBMED_CSV_FILE, CLINICAL_TRIALS_CSV_FILE

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_csv_files():
    """
    Load CSV datasets and return them as DataFrames.

    Returns:
        dict: A dictionary containing DataFrames for 'PubMed', 'ClinicalTrials', and 'Drugs'.
              If a file fails to load, its value will be None.
    """
    csv_files = {
        "PubMed": PUBMED_CSV_FILE,
        "ClinicalTrials": CLINICAL_TRIALS_CSV_FILE,
        "Drugs": DRUGS_FILE
    }

    dataframes = {}

    for name, file_path in csv_files.items():
        try:
            logging.info(f"📂 Loading {name} CSV file from: {file_path}...")
            df = load_csv(file_path)
            dataframes[name] = df
            logging.info(f"✔ {name} CSV loaded successfully. {df.shape[0]} rows found.")
        except FileNotFoundError:
            logging.error(f"❌ {name} CSV file not found at path: {file_path}")
            dataframes[name] = None
        except ValueError as e:
            logging.error(f"❌ Error loading {name} CSV: {e}")
            dataframes[name] = None

    return dataframes


import logging
import pandas as pd
from src.data_extract.extract import load_json
from src.config import PUBMED_JSON_FILE

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_json_file():
    """
    Load PubMed JSON dataset and return it as a DataFrame.

    Returns:
        pd.DataFrame or None: The loaded DataFrame if successful, otherwise None.
    """
    try:
        logging.info(f"📂 Loading PubMed JSON file from: {PUBMED_JSON_FILE}...")
        pubmed_json_df = load_json(PUBMED_JSON_FILE)
        logging.info(f"✔ PubMed JSON loaded successfully. {pubmed_json_df.shape[0]} rows found.")
        return pubmed_json_df

    except FileNotFoundError:
        logging.error(f"❌ PubMed JSON file not found at path: {PUBMED_JSON_FILE}")
    except ValueError as e:
        logging.error(f"❌ Error loading PubMed JSON: {e}")
    
    return None
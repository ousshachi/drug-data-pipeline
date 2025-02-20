import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame with error handling.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame or None: The loaded DataFrame, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)
        logging.info(f"✅ Successfully loaded CSV: {file_path} (Rows: {len(df)})")
        return df

    except FileNotFoundError:
        logging.error(f"❌ CSV file not found: {file_path}")
    except pd.errors.EmptyDataError:
        logging.warning(f"⚠ CSV file is empty: {file_path}")
    except pd.errors.ParserError:
        logging.error(f"❌ Failed to parse CSV file: {file_path}")
    except Exception as e:
        logging.error(f"❌ Unexpected error while loading CSV {file_path}: {e}", exc_info=True)

    return None  # Return None instead of raising an error

import pandas as pd
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_json(file_path: str) -> pd.DataFrame:
    """
    Load a JSON file into a Pandas DataFrame with error handling.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        pd.DataFrame or None: The loaded DataFrame, or None if an error occurs.
    """
    try:
        df = pd.read_json(file_path, encoding="utf-8")
        logging.info(f"✅ Successfully loaded JSON: {file_path} (Rows: {len(df)})")
        return df

    except FileNotFoundError:
        logging.error(f"❌ JSON file not found: {file_path}")
    except json.JSONDecodeError:
        logging.error(f"❌ Failed to parse JSON file: {file_path}")
    except Exception as e:
        logging.error(f"❌ Unexpected error while loading JSON {file_path}: {e}", exc_info=True)

    return None  # Return None instead of raising an error

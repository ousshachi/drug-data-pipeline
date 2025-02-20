import os

# Base directory for test data
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")
TEST_DATA_DIR_OUTPUT = os.path.join(os.path.dirname(__file__), "test_output")

# Paths to specific test files
CLINICAL_TRIALS_FILE = os.path.join(TEST_DATA_DIR, "clinical_trials.csv")
DRUGS_FILE = os.path.join(TEST_DATA_DIR, "drugs.csv")
PUBMED_CSV_FILE = os.path.join(TEST_DATA_DIR, "pubmed.csv")
PUBMED_JSON_FILE = os.path.join(TEST_DATA_DIR, "pubmed.json")
NON_EXISTANT_CSV_FILE = os.path.join(TEST_DATA_DIR, "non_existent.csv")
NON_EXISTANT_JSON_FILE = os.path.join(TEST_DATA_DIR, "non_existent.json")

# Path to output file
FILE_OUTPUT_PATH = os.path.join(TEST_DATA_DIR_OUTPUT, "test_drud_mention_graphe.json")
INVALID_JSON = os.path.join(TEST_DATA_DIR_OUTPUT, "invalid.json")
#TMP_DIR=  TEST_DATA_DIR_OUTPUT + '/nested/folder/'
#TMP_FILE =  os.path.join(TMP_DIR, "test_tmp.json")
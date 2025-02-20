import os

# Base directory for test data
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)  # Ensures it's an absolute path

# Directory for prepared data
PREPARED_DATA_DIR = os.path.join(DATA_DIR, 'data_preparation')
os.makedirs(PREPARED_DATA_DIR, exist_ok=True)

OUTPUT_DIR = 'output'
LINK_GRAPH_DIR = os.path.join(OUTPUT_DIR, 'link_graph')
AD_HOC_DIR = os.path.join(OUTPUT_DIR, 'ad_hoc')

# Paths to specific test files
DRUGS_FILE = os.path.join(DATA_DIR, "drugs.csv")
PUBMED_CSV_FILE = os.path.join(DATA_DIR, "pubmed.csv")
CLINICAL_TRIALS_CSV_FILE = os.path.join(DATA_DIR, "clinical_trials.csv") 
PUBMED_JSON_FILE = os.path.join(DATA_DIR, "pubmed.json")

# Fichiers après nettoyage
DRUGS_FILE_PREPARED = os.path.join(PREPARED_DATA_DIR, 'drugs.csv')
PUBMED_FILE_PREPARED = os.path.join(PREPARED_DATA_DIR, 'pubmed.csv')
PUBMED_JSON_FILE_PREPARED = os.path.join(PREPARED_DATA_DIR, 'pubmed.json')
CLINICAL_TRIALS_FILE_PREPARED = os.path.join(PREPARED_DATA_DIR, 'clinical_trials.csv')

# Dossiers de sortie
OUTPUT_JSON_PATH = os.path.join(LINK_GRAPH_DIR, 'drug_mentions_graph.json')
AD_HOC_OUTPUT_PATH = os.path.join(AD_HOC_DIR, 'most_mentioned_journal.json')

import os

# Base directory for test data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Paths to specific test files
DRUGS_FILE = os.path.join(DATA_DIR, "drugs.csv")
PUBMED_CSV_FILE = os.path.join(DATA_DIR, "pubmed.csv")
CLINICAL_TRIALS_CSV_FILE = os.path.join(DATA_DIR, "clinical_trials.csv")
PUBMED_JSON_FILE = os.path.join(DATA_DIR, "pubmed.json")

# Dossiers de sortie
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
LINK_GRAPH_DIR = os.path.join(OUTPUT_DIR, "link_graph")
AD_HOC_DIR = os.path.join(OUTPUT_DIR, "ad_hoc")

OUTPUT_JSON_PATH = os.path.join(LINK_GRAPH_DIR, "drug_mentions_graph.json")
AD_HOC_OUTPUT_PATH = os.path.join(AD_HOC_DIR, "most_mentioned_journal.json")
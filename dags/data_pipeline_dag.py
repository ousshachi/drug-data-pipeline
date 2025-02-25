import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

# Dynamically set the PROJECT_ROOT to the current directory (where this script is executed)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root folder to the Python path (where config.py is located)
sys.path.insert(0, project_root)

# Add src directory to Python path
sys.path.insert(0, os.path.join(project_root, "src"))

# Import config from root folder
from config import OUTPUT_JSON_PATH, AD_HOC_OUTPUT_PATH

# Check if the src directory is in the path
print("--------------------------------------------------------------------------")
print("project_root:", project_root)
print("PYTHONPATH:", os.getenv('PYTHONPATH', ''))
print("src Path:", os.path.join(project_root, "src"))
print("--------------------------------------------------------------------------")

# Import required modules from data_transform
from data_transform.data_processing import load_csv_files
from data_transform.drug_mentions import find_mentions
from data_transform.relationships import build_relationships
from data_transform.data_cleaning import clean_data

# Import required modules for ad-hoc analysis
from ad_hoc.ad_hoc import get_top_journal_by_unique_drugs

# Import the data_load module to save output
from data_load.load import save_to_json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="data_pipeline_dag",
    default_args=default_args,
    description="Data pipeline for processing drug mentions",
    schedule=None, # Désactive l'exécution automatique
    start_date=datetime(2025, 2, 21),
    catchup=False,
) as dag:

    def extract_data(**context):
        logging.info("=" * 50)
        logging.info("1- Starting data extraction process")
        logging.info("Loading CSV files...")

        loaded_dataframes = load_csv_files()
        logging.info(f"Extracted {len(loaded_dataframes)} dataframes")

        context['ti'].xcom_push(key='loaded_dataframes', value=loaded_dataframes)
        logging.info("Data extraction completed successfully")

    def transform_data(**context):
        logging.info("=" * 50)
        logging.info("2- Starting data transformation process")

        ti = context['ti']
        loaded_dataframes = ti.xcom_pull(task_ids='extract_data', key='loaded_dataframes')
        logging.info(f"Retrieved {len(loaded_dataframes)} dataframes from previous task")

        logging.info("Cleaning data...")
        cleaned_data_df = clean_data(loaded_dataframes)
        logging.info("Data cleaning completed")

        logging.info("3- Finding drug mentions in publications...")
        mentions = find_mentions(
            cleaned_data_df["PubMed"],
            cleaned_data_df["ClinicalTrials"],
            cleaned_data_df["Drugs"],
        )
        logging.info(f"Found {len(mentions)} drug mentions")

        logging.info("4- Building relationships...")
        relationships = build_relationships(mentions)
        logging.info("Relationships built successfully")

        ti.xcom_push(key='relationships', value=relationships)
        logging.info("Data transformation completed successfully")

    def load_data(**context):
        logging.info("=" * 50)
        logging.info("5- Starting data loading process")

        ti = context['ti']
        relationships = ti.xcom_pull(task_ids='transform_data', key='relationships')
        logging.info(f"Retrieved relationships data from previous task")

        logging.info(f"6- Saving final JSON output to {OUTPUT_JSON_PATH}...")
        print(f"6- Saving final JSON output to {OUTPUT_JSON_PATH}...")
        save_to_json(relationships, OUTPUT_JSON_PATH)
        logging.info("JSON output saved successfully")

        logging.info("7- Generating ad-hoc analysis...{''}\n")
        dataframe_df = get_top_journal_by_unique_drugs(OUTPUT_JSON_PATH)
        logging.info("Ad-hoc analysis completed")
    
        logging.info(f"8- Saving ad-hoc file to {AD_HOC_OUTPUT_PATH}...")
        save_to_json(dataframe_df, AD_HOC_OUTPUT_PATH)
        logging.info("Ad-hoc file saved successfully")

        logging.info("✅ Data processing pipeline completed successfully")

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
        dag=dag
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        dag=dag
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
        dag=dag
    )

    # Set task dependencies
    extract_task >> transform_task >> load_task

logging.info("DAG 'data_pipeline_dag' has been defined")
# Variables
PYTHON = python
PIP = pip
VENV = venv
ACTIVATE = source $(VENV)/bin/activate
SRC_DIR = src
TEST_DIR = tests
DAGS_DIR = dags
AIRFLOW_HOME = $(PWD)/airflow
PROJECT_DIR = $(PWD)
LINK_GRAPH_DIRECTORY =output/link_graph 
AD_HOC_DIRECTORY = output/ad_hoc


# Add project root to PYTHONPATH
export PYTHONPATH := $(PROJECT_DIR):$(PYTHONPATH)

.PHONY: all
all: install format lint  test run-pipeline airflow-init airflow-start deploy-dags clean

# Default target (help message)
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install         Install dependencies"
	@echo "  make lint            Run Flake8 for linting"
	@echo "  make format          Format code with Black"
	@echo "  make test            Run all tests with pytest"
	@echo "  make test-unit       Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make run-pipeline    Run the data pipeline locally"
	@echo "  make airflow-init    Initialize Airflow database and setup"
	@echo "  make airflow-start   Start Airflow webserver and scheduler"
	@echo "  make airflow-stop    Stop all running Airflow processes"
	@echo "  make deploy-dags      Create DAG folder and deploy DAGs"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Code formatting with Black
.PHONY: format
format:
	black $(SRC_DIR) $(TEST_DIR)

# Linting with Flake8
.PHONY: lint
lint:
	flake8 $(SRC_DIR) $(TEST_DIR)

#.PHONY: test
test:
	pytest $(SRC_DIR) $(TEST_DIR)	

# Run unit tests only
.PHONY: test-unit
#test-unit:
	pytest $(TEST_DIR)/unit

# Run integration tests only
.PHONY: test-integration
test-integration:
	pytest $(TEST_DIR)/integration

# Run the data pipeline locally
.PHONY: run-pipeline
run-pipeline:
	# Create the necessary output directories
	mkdir -p $(PROJECT_DIR)/$(LINK_GRAPH_DIRECTORY) $(PROJECT_DIR)/$(AD_HOC_DIRECTORY)
	# Run the DAG
	dotenv run -- $(PYTHON) $(DAGS_DIR)/data_pipeline_dag.py

# Airflow initialization (database setup)
.PHONY: airflow-init
airflow-init:
	mkdir -p $(AIRFLOW_HOME) && chmod 755 $(AIRFLOW_HOME)
	AIRFLOW_HOME=$(AIRFLOW_HOME) airflow db init && \
	AIRFLOW_HOME=$(AIRFLOW_HOME) airflow users create \
		--username admin \
		--password admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com

# Start Airflow services (webserver and scheduler)
.PHONY: airflow-start
airflow-start:
	@echo "Starting Airflow..."
	export AIRFLOW_HOME=$(AIRFLOW_HOME) && \
	nohup airflow webserver --port 8080 > airflow-webserver.log 2>&1 & \
	nohup airflow scheduler > airflow-scheduler.log 2>&1 & \
	echo "Airflow started! Logs: airflow-webserver.log, airflow-scheduler.log"

# Stop Airflow services
.PHONY: airflow-stop
airflow-stop:
	@echo "Stopping Airflow..."
	pkill -f "airflow webserver"
	pkill -f "airflow scheduler"
	@echo "Airflow stopped."

# Deploy DAGs: create DAG folder and copy DAG file
.PHONY: deploy-dags
deploy-dags:
	@echo "Creating DAG folder if it doesn't exist..."
	mkdir -p $(AIRFLOW_HOME)/dags
	@echo "Deploying DAG to $(AIRFLOW_HOME)/dags..."
	cp $(PROJECT_DIR)/dags/data_pipeline_dag.py $(AIRFLOW_HOME)/dags/

# Clean up temporary files and cache
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
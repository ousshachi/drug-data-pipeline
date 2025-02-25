# Variables
PYTHON = python
PIP = pip
VENV = myvenv
ACTIVATE = . $(VENV)/bin/activate
SRC_DIR = src
TEST_DIR = tests
DAGS_DIR = dags
PROJECT_DIR = $(PWD)
AIRFLOW_HOME = $(PROJECT_DIR)/airflow
PIPELINE_PROJECT = $(PROJECT_DIR)/dags/data_pipeline_dag.py

# Add project root to PYTHONPATH
export PYTHONPATH := $(PROJECT_DIR):$(PROJECT_DIR)/src

.PHONY: all
all: display_variables install format lint test run_pipeline airflow_init airflow_start deploy_dags clean

# Default target (help message)
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install          Install dependencies"
	@echo "  make lint             Run Flake8 for linting"
	@echo "  make format           Format code with Black"
	@echo "  make test             Run all tests with pytest"
	@echo "  make run_pipeline     Run the data pipeline locally"
	@echo "  make airflow_init     Initialize Airflow database and setup"
	@echo "  make airflow_start    Start Airflow webserver and scheduler"
	@echo "  make airflow_stop     Stop all running Airflow processes"
	@echo "  make deploy_dags      Deploy DAGs to Airflow"

.PHONY: display_variables
display_variables:
	@echo ################################################################################
	@echo PROJECT_DIR = $(PROJECT_DIR)
	@echo AIRFLOW_HOME = $(AIRFLOW_HOME)
	@echo PIPELINE_PROJECT = $(PIPELINE_PROJECT)
	@echo ################################################################################

# Install dependencies into the virtual environment
.PHONY: install
install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found, creating..."; \
		$(PYTHON) -m venv $(VENV); \
	fi
	. $(VENV)/bin/activate && $(PIP) install --upgrade pip
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt

# Code formatting with Black
.PHONY: format
format:
	black $(SRC_DIR) $(TEST_DIR)

# Linting with Flake8
.PHONY: lint
lint:
	flake8 $(SRC_DIR) $(TEST_DIR)

# Run tests
.PHONY: test
test:
	pytest $(SRC_DIR) $(TEST_DIR)

# Run the data pipeline locally
.PHONY: run_pipeline
run_pipeline:
	@echo "Running DAG: $(PIPELINE_PROJECT)"
	@echo "Using Python: $(PYTHON)"
	dotenv run -- $(PYTHON) $(PIPELINE_PROJECT)

# Airflow initialization (database setup)
.PHONY: airflow_init
airflow_init:
	@echo "Initializing Airflow..."
	export AIRFLOW_HOME=$(AIRFLOW_HOME) && \
	mkdir -p $$AIRFLOW_HOME && chmod 755 $$AIRFLOW_HOME && \
	airflow db init && \
	airflow users create \
		--username admin \
		--password admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com

# Start Airflow services (webserver and scheduler)
.PHONY: airflow_start
airflow_start:
	@echo "Starting Airflow..."
	export AIRFLOW_HOME=$(AIRFLOW_HOME) && \
	nohup airflow webserver --port 8080 > $$AIRFLOW_HOME/airflow-webserver.log 2>&1 & \
	nohup airflow scheduler > $$AIRFLOW_HOME/airflow-scheduler.log 2>&1 & \
	echo "Airflow started! Logs: $$AIRFLOW_HOME/airflow-webserver.log, $$AIRFLOW_HOME/airflow-scheduler.log"

# Stop Airflow services
.PHONY: airflow_stop
airflow_stop:
	@echo "Stopping Airflow..."
	pkill -f "airflow webserver"
	pkill -f "airflow scheduler"
	@echo "Airflow stopped."

# Deploy DAGs: create DAG folder and copy DAG file
.PHONY: deploy_dags
deploy_dags:
	@echo "Deploying DAG to Airflow..."
	export AIRFLOW_HOME=$(AIRFLOW_HOME) && \
	mkdir -p $$AIRFLOW_HOME/dags && \
	cp $(PIPELINE_PROJECT) $$AIRFLOW_HOME/dags/
	@echo "DAG successfully deployed to $$AIRFLOW_HOME/dags/"

# Clean up temporary files and cache
.PHONY: clean
clean:
	sudo find . -type f -name "*.py[co]" ! -path "./$(VENV)/*" -delete
	sudo find . -type d -name "__pycache__" ! -path "./$(VENV)/*" -prune -exec rm -rf {} +
# drug-data-pipeline

This repository is a data pipeline project designed to process and analyze drug-related data from various sources.

## Créer un environnement virtuel Python 3.11.x sous WSL

Pour créer un environnement virtuel Python 3.11.x sous WSL (Windows Subsystem for Linux), suivez les étapes suivantes :

### Vérifier la version de Python installée

- Ouvrez votre terminal WSL.
- Exécutez la commande suivante pour vérifier la version de Python :


<pre><code>python --version</code></pre>


Si la version affichée est inférieure à 3.11.x, vous devrez installer Python 3.11.x.

### Installer Python 3.11.x

- Ajoutez le dépôt de paquets de Python :

<pre><code>sudo add-apt-repository ppa:deadsnakes/ppa</code></pre>


- Mettez à jour la liste des paquets :

<pre><code>sudo apt update</code></pre>

- Installez Python 3.11 :

<pre><code>sudo apt install python3.11</code></pre>


- Vérifiez l'installation :

<pre><code>python3.11 --version</code></pre>


### Installer python3.11-venv

- Installez le module venv pour Python 3.11 :

<pre><code>sudo apt install python3.11-venv</code></pre>


### Créer un environnement virtuel

- Naviguez vers le répertoire de votre projet :

<pre><code>cd /chemin/vers/votre/projet</code></pre>
 Exemple : *cd /home/user/data_pipeline_project*

<pre><code>python3.11 -m venv nom_de_votre_env</code></pre>
 Exemple : *python3.11 -m venv venv*

Remplacez `nom_de_votre_env` par le nom souhaité pour votre environnement virtuel.

- Activez l'environnement :

<pre><code>source nom_de_votre_env/bin/activate</code></pre>
 Exemple: *source venv/bin/activate*

Vous devriez voir le nom de l'environnement virtuel apparaître dans votre invite de commande, indiquant que l'environnement est activé.

### Remarques

- Assurez-vous que votre système est à jour avant d'installer de nouveaux paquets :

<pre><code>sudo apt update && sudo apt upgrade</code></pre>


## Installer les dépendances listées dans un fichier requirements.txt

Pour installer les dépendances listées dans un fichier `requirements.txt` sous Python 3.11.x, suivez les étapes suivantes :

### Assurez-vous que votre environnement virtuel est activé

- Si vous n'avez pas encore créé d'environnement virtuel, créez-en un avec la commande :

<pre><code>python3.11 -m venv mon_env</code></pre>
Exemple : *python3.11 -m venv venv*


Remplacez `mon_env` par le nom souhaité pour votre environnement virtuel.

- Activez l'environnement virtuel :

<pre><code>source mon_env/bin/activate</code></pre>
Exemple : *source venv/bin/activate*

Vous devriez voir le nom de l'environnement virtuel apparaître dans votre invite de commande, indiquant que l'environnement est activé.

### Installez les dépendances à partir du fichier requirements.txt

- Assurez-vous que le fichier `requirements.txt` est présent dans le répertoire courant.

- Installez les packages listés dans le fichier :

<pre><code>pip install -r requirements.txt</code></pre>


Cette commande lira le fichier `requirements.txt` et installera toutes les dépendances spécifiées.

### Remarque

- Si vous rencontrez des problèmes lors de l'installation des packages, il est possible que votre système empêche l'installation de packages Python non gérés par le système. Pour contourner ce problème, vous pouvez utiliser l'option `--break-system-packages` avec pip :

<pre><code>pip install --break-system-packages -r requirements.txt</code></pre>


## Exécuter pytest

Pour exécuter pytest, identifiez le répertoire src :

<pre><code>export PYTHONPATH="/home/user/myproject:$PYTHONPATH"</code></pre>
Exemple : *export PYTHONPATH="/home/user/data_pipeline_project:$PYTHONPATH"*


Vérifiez la variable d'environnement :

<pre><code>echo $PYTHONPATH</code></pre>


### Méthode permanente

Pour que cette modification soit persistante, ajoutez la ligne suivante à la fin de votre fichier `~/.bashrc` :

<pre><code>source ~/.bashrc</code></pre>


# Project Structure
<pre><code>
DATA_PIPELINE_PROJECT
├── data
├── myvenv
├── sql_queries
├    └── query1
├    └── query2
├── src
│   ├── ad_hoc
│   │   ├── __init__.py
│   │   └── ad_hoc.py
│   ├── data_extract
│   │   ├── __init__.py
│   │   └── extract.py
│   ├── data_load
│   │   ├── __init__.py
│   │   ├── load.py
│   ├── data_transform
│   │   └── utils
│   │   |  ├── __init__.py
│   │   ├  └── utils.py
│   │   ├── __init__.py
│   │   ├── data_cleaning.py
│   │   ├── data_processing.py
│   │   ├── drug_mentions.py
│   │   ├── relationships.py
│   ├── config.py
│   └── main.py
├── tests
│   ├── test_output
│   └── unit
│       └── config_test.py
├── .gitignore
├── POUR_ALLER_PLUS_LOIN.md
├── pyproject.toml
├── pytest.ini
├── README.md
└── requirements.txt
</code></pre>

### Execute all tests
Se placer dans le reperoire de votre projet : /home/user/data_pipeline_project*
<pre><code>pytest</code></pre>


### Execute a specific test
 Se placer dans le reperoire de test : *cd /home/user/data_pipeline_project/tests/unit*
<pre><code>
  pytest name_of_the_test.py    
</code></pre>

### Run Program
 Se placer dans le reperoire src de votre project : *cd /home/user/data_pipeline_project/src*
<pre><code>
  pyton main.py 
</code></pre>

###  outputs
2 fichiers sont générés dans le dossier output ( crée par le programme) : */home/user/data_pipeline/output*
Les deux fichiers sont chacun dans un dossier : link_graph pour *drug_mentions_graph.json* et ad_hoc pour *most_mentioned_journal.json*
<pre><code>
   home/user/data_pipeline/output/link_graph/drug_mentions_graph.json
   home/user/data_pipeline/output/ad_hoc/most_mentioned_journal.json
</code></pre>

###  Execute Dag
Se placer dans le reperoire de votre projet : */home/user/data_pipeline_project* et executer le MakeFile
<pre><code>
   make
</code></pre>

###  Vérifier les variable d'environement de votre système et modifer si necessaire avec les commandes ci dessous
Se placer dans le reperoire de votre projet : */home/user/data_pipeline_project* et executer le MakeFile
<pre><code>
   echo $AIRFLOW_HOME
   echo $PATH
   export AIRFLOW_HOME=/home/user/data_pipeline_project/airflow
   export PATH=/home/user/data_pipeline_project/venv/bin:$PATH
</code></pre>

En cas de problem stop airflow
<pre><code>
  make airflow-stop
</code></pre>

Relancer airflow avec la cammande make : (la commande *make* démarre airflow grace à la commande make *airflow-start*)
<pre><code>
  make
</code></pre>

###  Ouvrir le navigateur avec l'url : http://localhost:8080/home
### Aller sur le dag data_pipeline_dag avec l'url :  http://localhost:8080/dags/data_pipeline_dag/grid
### Lancer le job : avec le boutton trigger DAG
### Suivre l'execution du job

###  outputs
2 fichiers sont générés dans le dossier output ( crée par le programme) : */home/user/data_pipeline/output*
Les deux fichiers sont chacun dans un dossier : link_graph pour *drug_mentions_graph.json* et ad_hoc pour *most_mentioned_journal.json*
<pre><code>
   home/user/data_pipeline/output/link_graph/drug_mentions_graph.json
   home/user/data_pipeline/output/ad_hoc/most_mentioned_journal.json
</code></pre>


###  Pour aller plus loin
[Réponse suir la question pour aller plus loin : cliquez ici ](POUR_ALLER_PLUS_LOIN.md)

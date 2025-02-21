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

sudo add-apt-repository ppa:deadsnakes/ppa


- Mettez à jour la liste des paquets :

sudo apt update

- Installez Python 3.11 :

sudo apt install python3.11


- Vérifiez l'installation :

python3.11 --version


### Installer python3.11-venv

- Installez le module venv pour Python 3.11 :

sudo apt install python3.11-venv


### Créer un environnement virtuel

- Naviguez vers le répertoire de votre projet :

cd /chemin/vers/votre/projet

python3.11 -m venv nom_de_votre_env


Remplacez `nom_de_votre_env` par le nom souhaité pour votre environnement virtuel.

- Activez l'environnement :

source nom_de_votre_env/bin/activate

Vous devriez voir le nom de l'environnement virtuel apparaître dans votre invite de commande, indiquant que l'environnement est activé.

### Remarques

- Assurez-vous que votre système est à jour avant d'installer de nouveaux paquets :

sudo apt update && sudo apt upgrade

text

## Installer les dépendances listées dans un fichier requirements.txt

Pour installer les dépendances listées dans un fichier `requirements.txt` sous Python 3.11.x, suivez les étapes suivantes :

### Assurez-vous que votre environnement virtuel est activé

- Si vous n'avez pas encore créé d'environnement virtuel, créez-en un avec la commande :

python3.11 -m venv mon_env

text

Remplacez `mon_env` par le nom souhaité pour votre environnement virtuel.

- Activez l'environnement virtuel :

source mon_env/bin/activate

text

Vous devriez voir le nom de l'environnement virtuel apparaître dans votre invite de commande, indiquant que l'environnement est activé.

### Installez les dépendances à partir du fichier requirements.txt

- Assurez-vous que le fichier `requirements.txt` est présent dans le répertoire courant.

- Installez les packages listés dans le fichier :

pip install -r requirements.txt

text

Cette commande lira le fichier `requirements.txt` et installera toutes les dépendances spécifiées.

### Remarque

- Si vous rencontrez des problèmes lors de l'installation des packages, il est possible que votre système empêche l'installation de packages Python non gérés par le système. Pour contourner ce problème, vous pouvez utiliser l'option `--break-system-packages` avec pip :

pip install --break-system-packages -r requirements.txt

text

## Exécuter pytest

Pour exécuter pytest, identifiez le répertoire src :

export PYTHONPATH="/home/user/myproject:$PYTHONPATH"

text

Exemple :

export PYTHONPATH="/home/ohachi/data_pipeline_project:$PYTHONPATH"

text

Vérifiez la variable d'environnement :

echo $PYTHONPATH

text

### Méthode permanente

Pour que cette modification soit persistante, ajoutez la ligne suivante à la fin de votre fichier `~/.bashrc` :

source ~/.bashrc

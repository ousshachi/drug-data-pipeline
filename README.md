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

<pre><code>python3.11 -m venv nom_de_votre_env</code></pre>


Remplacez `nom_de_votre_env` par le nom souhaité pour votre environnement virtuel.

- Activez l'environnement :

<pre><code>source nom_de_votre_env/bin/activate</code></pre>

Vous devriez voir le nom de l'environnement virtuel apparaître dans votre invite de commande, indiquant que l'environnement est activé.

### Remarques

- Assurez-vous que votre système est à jour avant d'installer de nouveaux paquets :

<pre><code>sudo apt update && sudo apt upgrade</code></pre>


## Installer les dépendances listées dans un fichier requirements.txt

Pour installer les dépendances listées dans un fichier `requirements.txt` sous Python 3.11.x, suivez les étapes suivantes :

### Assurez-vous que votre environnement virtuel est activé

- Si vous n'avez pas encore créé d'environnement virtuel, créez-en un avec la commande :

<pre><code>python3.11 -m venv mon_env</code></pre>


Remplacez `mon_env` par le nom souhaité pour votre environnement virtuel.

- Activez l'environnement virtuel :

<pre><code>source mon_env/bin/activate</code></pre>


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


Vérifiez la variable d'environnement :

<pre><code>echo $PYTHONPATH</code></pre>


### Méthode permanente

Pour que cette modification soit persistante, ajoutez la ligne suivante à la fin de votre fichier `~/.bashrc` :

<pre><code>source ~/.bashrc</code></pre>

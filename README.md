# mangbralouma

association familiale

Application Python (CLI + Web) pour gerer les membres de la grande famille,
les cotisations et les evenements.

## Description

Ce depot contient une application en ligne de commande (CLI) et une
application web Flask avec stockage JSON local.
L'objectif est d'avoir une base operationnelle pour l'association familiale:

- enregistrer les membres
- suivre les cotisations
- planifier les evenements
- afficher un resume global

## Fonctionnement actuel

La CLI propose des commandes metier:

- `init`: initialise la base locale
- `member add|list`: ajoute et affiche les membres
- `cotisation add|list`: ajoute et affiche les cotisations
- `event add|list`: ajoute et affiche les evenements avec raison et montant
- `summary`: affiche les indicateurs principaux

L'application web propose des formulaires pour les memes operations.

## Demarrage rapide

Cloner le depot :

```bash
git clone https://github.com/valamameite-hash/mangbralouma
cd mangbralouma
```

Activer l'environnement virtuel sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer le projet en mode editable :

```bash
pip install -e .
```

Installer les dependances de test :

```bash
pip install -e .[test]
```

Lancer l'aide :

```bash
python -m mangbralouma --help
```

Initialiser la base locale :

```bash
mangbralouma init
```

Ajouter un membre :

```bash
mangbralouma member add --first-name "Aicha" --last-name "Traore" --nickname "Aichou" --country "Mali" --city "Bamako" --occupation "Commercante" --phone "+22300000000" --email "aicha@example.com"
```

Ajouter une cotisation :

```bash
mangbralouma cotisation add --member-id 1 --amount 5000 --date 2026-03-17 --note "Cotisation mars"
```

Ajouter un evenement :

```bash
mangbralouma event add --title "Reunion generale" --date 2026-04-05 --reason mariage --amount 15000 --description "Maison familiale"
```

Raisons disponibles pour un evenement:

- `funerailles`
- `mariage`
- `baptemes`
- `sacrifices`
- `autres`

Afficher le resume :

```bash
mangbralouma summary
```

## Application web

Installer le projet:

```bash
pip install -e .
```

Demarrer le serveur web en local:

```bash
mangbralouma-web --host 127.0.0.1 --port 5000
```

Ouvrir dans le navigateur:

```text
http://127.0.0.1:5000
```

### Acces depuis un autre ordinateur (meme reseau)

Demarrer le serveur avec ecoute reseau:

```bash
mangbralouma-web --host 0.0.0.0 --port 5000
```

Trouver l'IP locale du PC serveur (exemple `192.168.1.25`) avec:

```powershell
ipconfig
```

Depuis l'autre ordinateur, ouvrir:

```text
http://192.168.1.25:5000
```

Important:

- Les deux ordinateurs doivent etre sur le meme reseau.
- Autoriser le port `5000` dans le pare-feu Windows si necessaire.
- Si l'IP change, reutiliser `ipconfig` pour verifier la nouvelle adresse.

## Structure du projet

```text
mangbralouma/
|-- README.md
|-- pyproject.toml
|-- src/
|   `-- mangbralouma/
|       |-- __init__.py
|       |-- __main__.py
|       |-- main.py
|       |-- web.py
|       `-- templates/
|           `-- index.html
`-- tests/
    |-- conftest.py
    |-- test_main.py
    `-- test_web.py
```

## Tests

Des tests unitaires couvrent la CLI et les routes web principales.

```bash
pytest
```

CI GitHub Actions est configuree pour lancer les tests automatiquement a chaque push et pull request.

## Workflow Git

```bash
git add .
git commit -m "Votre message de commit"
git push
```

Verifier l'etat du depot :

```bash
git status
```

## Roadmap

- ajouter l'edition et la suppression des membres
- exporter les rapports mensuels (CSV/PDF)
- ajouter des roles (tresorier, secretaire, admin)

## Auteur

Nom Git : mangbralouma

Email Git : valamameite@gmail.com

## Depot distant

GitHub : https://github.com/valamameite-hash/mangbralouma

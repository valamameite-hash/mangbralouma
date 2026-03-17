# mangbralouma

association familiale

Application CLI Python pour gerer les membres de la grande famille, les cotisations et les evenements.

## Description

Ce depot contient une application en ligne de commande (CLI) avec stockage JSON local.
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
- `event add|list`: ajoute et affiche les evenements
- `summary`: affiche les indicateurs principaux

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
mangbralouma member add --name "Aicha" --phone "+22300000000" --email "aicha@example.com"
```

Ajouter une cotisation :

```bash
mangbralouma cotisation add --member-id 1 --amount 5000 --date 2026-03-17 --note "Cotisation mars"
```

Ajouter un evenement :

```bash
mangbralouma event add --title "Reunion generale" --date 2026-04-05 --description "Maison familiale"
```

Afficher le resume :

```bash
mangbralouma summary
```

## Structure du projet

```text
mangbralouma/
|-- README.md
|-- pyproject.toml
|-- src/
|   `-- mangbralouma/
|       |-- __init__.py
|       |-- __main__.py
|       `-- main.py
`-- tests/
    |-- conftest.py
    `-- test_main.py
```

## Tests

Des tests unitaires couvrent la creation de base, l'ajout de membres, la validation des cotisations et le resume.

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

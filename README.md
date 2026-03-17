# mangbralouma

Base de projet Python initialisee et connectee a GitHub.

## Description

Ce depot contient un squelette de projet Python simple, pret a etre etendu.
Il fournit une structure claire avec un package applicatif dans `src/`, un dossier `tests/` et la configuration minimale du projet dans `pyproject.toml`.

## Fonctionnement actuel

Le projet expose pour l'instant un point d'entree minimal qui affiche un message de confirmation.
Cela permet de verifier que la structure Python est correcte avant d'ajouter les vraies fonctionnalites.

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

Lancer le module principal :

```bash
python -m mangbralouma.main
```

## Structure du projet

```text
mangbralouma/
|-- README.md
|-- pyproject.toml
|-- src/
|   `-- mangbralouma/
|       |-- __init__.py
|       `-- main.py
`-- tests/
	`-- test_main.py
```

## Tests

Un test minimal est fourni pour verifier le point d'entree principal.

```bash
pytest
```

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

- Remplacer le point d'entree d'exemple par la logique metier
- Ajouter de nouveaux modules dans `src/mangbralouma`
- Etendre la suite de tests
- Documenter l'installation et l'utilisation reelle du projet

## Auteur

Nom Git : mangbralouma

Email Git : valamameite@gmail.com

## Depot distant

GitHub : https://github.com/valamameite-hash/mangbralouma
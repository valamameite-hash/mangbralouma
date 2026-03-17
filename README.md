# mangbralouma

association familiale

Base de projet Python initialisee et connectee a GitHub.

## Description

Ce depot contient un squelette de projet Python simple, pret a etre etendu.
Il fournit une structure claire avec un package applicatif dans `src/`, un dossier `tests/`, une petite interface en ligne de commande et la configuration minimale du projet dans `pyproject.toml`.

## Fonctionnement actuel

Le projet expose maintenant une CLI minimale qui affiche un message configurable.
Cela permet de verifier que la structure Python, l'entree applicative et les tests sont correctement relies.

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

Lancer le module principal :

```bash
python -m mangbralouma
```

Executer la commande CLI installee :

```bash
mangbralouma --name demo
```

Exemple avec majuscules :

```bash
mangbralouma --name demo --upper
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

Des tests minimaux sont fournis pour verifier le message genere et le comportement de la CLI.

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

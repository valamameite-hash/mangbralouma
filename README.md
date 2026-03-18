# mangbralouma

association familiale

Application Python (CLI) pour gerer les membres de la grande famille,
les cotisations et les evenements.

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
- `member add|list|search|update|delete|deactivate|reactivate`: gerer les membres
- `cotisation add|list|report`: gerer les cotisations et rapports
- `event add|list|add-attendee`: gerer les evenements et participants
- `export --type <members|cotisations|events>`: exporter les donnees en CSV
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

Rechercher un membre :

```bash
mangbralouma member search --query "Aichou"
```

Mettre a jour un membre :

```bash
mangbralouma member update --id 1 --phone "+22300000001"
```

Desactiver un membre :

```bash
mangbralouma member deactivate --id 1
```

Supprimer un membre :

```bash
mangbralouma member delete --id 1
```

Generer un rapport de cotisations :

```bash
mangbralouma cotisation report --member-id 1
```

Ajouter un participant a un evenement :

```bash
mangbralouma event add-attendee --event-id 1 --member-id 2
```

Exporter les donnees en CSV :

```bash
mangbralouma export --type members
mangbralouma export --type cotisations
mangbralouma export --type events
```

Les fichiers CSV sont generes dans le repertoire courant.

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

Des tests unitaires couvrent la CLI et les principales operations.

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

- ajouter des rapports mensuels ou annuels
- exporter en PDF
- ajouter des roles (tresorier, secretaire, admin)
- statistiques avancees par periode

## Auteur

Nom Git : mangbralouma

Email Git : valamameite@gmail.com

## Depot distant

GitHub : https://github.com/valamameite-hash/mangbralouma

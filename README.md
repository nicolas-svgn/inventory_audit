# Inventory Audit Project

Ce projet automatise l'analyse de cohérence entre le catalogue article (`ARTOKM`), le référentiel des familles (`Famille`) et les positions de stock actuelles (`PositionOKM`).

## Prérequis
* **Python version** : `3.10.12`
* **Bibliothèques** : `pandas`

## Structure du Projet



```text
inventory_audit/
├── data/               # Fichiers CSV sources (ARTOKM, Famille, PositionOKM)
├── output/             # Résultats de l'audit générés en CSV
├── src/                # Code source modulaire
│   ├── __init__.py
│   └── audit_logic.py  # Fonctions de nettoyage et de calcul
├── venv/               # Environnement virtuel (exclu de Git)
├── .gitignore          # Liste des fichiers à ignorer par Git
├── main.py             # Point d'entrée principal du programme
└── requirements.txt    # Liste des dépendances Python

## Installation et Exécution

### 1. Cloner et configurer l'environnement
Ouvrez un terminal dans le dossier du projet :

```bash
# Création de l'environnement virtuel
python3 -m venv venv

# Activation de l'environnement (Linux/Mac)
source venv/bin/activate

# Installation des dépendances
pip install -r requirements.txt
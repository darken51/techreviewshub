#!/bin/bash

# 🤖 Script pour lancer l'automatisation avec token sécurisé
# Usage: ./run_automation.sh

echo "🤖 TECH REVIEWS HUB - Automatisation"
echo "===================================="
echo ""

# Vérifier si le token est défini
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  Variable GITHUB_TOKEN non définie"
    echo ""
    echo "Pour définir le token:"
    echo "  export GITHUB_TOKEN='ghp_VotreTokenIci'"
    echo ""
    echo "Ou créer un fichier .env:"
    echo "  echo 'GITHUB_TOKEN=ghp_VotreTokenIci' > .env"
    echo "  source .env"
    echo ""
    exit 1
fi

echo "✅ Token GitHub détecté"
echo ""

# Exécuter l'automatisation
python3 automate_all.py

echo ""
echo "✅ Automatisation terminée"

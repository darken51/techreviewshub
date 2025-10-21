#!/bin/bash
# Script d'automatisation de mise à jour des prix Amazon
# À exécuter via cron (recommandé : 1x par semaine)

set -e  # Arrêter si erreur

# Configuration
SITE_DIR="/home/fred/techreviewshub-site"
LOG_FILE="$SITE_DIR/price_update.log"
TIMESTAMP=$(date +'%Y-%m-%d %H:%M:%S')

echo "=== Début de la mise à jour des prix - $TIMESTAMP ===" >> "$LOG_FILE"

# Se déplacer dans le répertoire du site
cd "$SITE_DIR"

# Activer le virtual environment si présent
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Exécuter le script de mise à jour des prix
python3 amazon_price_updater.py >> "$LOG_FILE" 2>&1

# Vérifier si des fichiers ont été modifiés
if ! git diff --quiet; then
    echo "📝 Des prix ont été mis à jour, création d'un commit..." >> "$LOG_FILE"

    # Ajouter les fichiers modifiés
    git add *_review.html price_history.log

    # Créer le commit
    git commit -m "Update: Prix Amazon mis à jour automatiquement le $(date +'%Y-%m-%d')

🤖 Mise à jour automatique via cron
📊 Voir price_history.log pour les détails" >> "$LOG_FILE" 2>&1

    # Pousser vers GitHub (nécessite GITHUB_TOKEN en variable d'environnement)
    if [ -n "$GITHUB_TOKEN" ]; then
        git push https://$GITHUB_TOKEN@github.com/darken51/techreviewshub.git main >> "$LOG_FILE" 2>&1
        echo "✅ Changements poussés vers GitHub" >> "$LOG_FILE"
    else
        echo "⚠️  GITHUB_TOKEN non défini, push manuel requis" >> "$LOG_FILE"
    fi
else
    echo "ℹ️  Aucun changement de prix détecté" >> "$LOG_FILE"
fi

echo "=== Fin de la mise à jour - $(date +'%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

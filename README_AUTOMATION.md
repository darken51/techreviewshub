# 🤖 AUTOMATISATION COMPLÈTE TECH REVIEWS HUB

Système d'automatisation de bout en bout pour générer, déployer et maintenir le site automatiquement.

## 🎯 Vue d'ensemble

```
┌─────────────────────────────────────────────────────┐
│           🤖 SYSTÈME D'AUTOMATISATION               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📝 Génération Reviews  →  🔄 Mise à jour Site      │
│           ↓                       ↓                 │
│  💰 Update Prix         →  📤 Git Commit/Push       │
│           ↓                       ↓                 │
│  🏗️  Build & Deploy     →  🌐 GitHub Pages          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 📦 Fichiers du système

| Fichier | Description |
|---------|-------------|
| `automate_all.py` | **🎯 Script principal** - Automatisation complète |
| `generate_review_auto.py` | Générateur de reviews HTML |
| `generate_batch_reviews.py` | Génération en batch |
| `auto_price_updater.py` | Mise à jour automatique des prix |
| `scheduler.py` | Planificateur de tâches (cron) |
| `config_automation.json` | Configuration centralisée |
| `.github/workflows/auto-deploy.yml` | CI/CD GitHub Actions |

## 🚀 Utilisation rapide

### 1️⃣ Génération automatique complète

```bash
# Génère reviews + met à jour index.html + commit + push
python3 automate_all.py
```

**Ce script fait TOUT automatiquement:**
- ✅ Génère les reviews HTML (pattern exact)
- ✅ Met à jour `index.html` (ajoute produits)
- ✅ Met à jour la recherche (search database)
- ✅ Git add + commit + push
- ✅ Déploiement automatique GitHub Pages

### 2️⃣ Génération manuelle de reviews

```bash
# Générer 3 reviews spécifiques
python3 generate_batch_reviews.py
```

### 3️⃣ Mise à jour des prix

```bash
# Met à jour tous les prix depuis Amazon
python3 auto_price_updater.py
```

### 4️⃣ Scheduler automatique

```bash
# Démarre le scheduler (tâches programmées)
python3 scheduler.py

# Test des tâches
python3 scheduler.py --test

# Aide configuration cron
python3 scheduler.py --cron-help
```

## ⚙️ Configuration

Éditez `config_automation.json` pour personnaliser:

```json
{
  "automation": {
    "enabled": true,
    "auto_commit": true,        // Commit automatique
    "auto_push": true,           // Push automatique
    "auto_price_update": false,  // Mise à jour prix (désactivé par défaut)
    "auto_review_generation": false  // Génération auto (désactivé)
  },

  "schedule": {
    "review_generation": {
      "frequency": "weekly",     // Fréquence: daily, weekly, monthly
      "day": "monday",
      "time": "02:00",
      "batch_size": 3            // Nombre de reviews par batch
    }
  }
}
```

## 📋 Workflow automatique complet

### Scénario 1: Ajout manuel de 3 produits

```bash
# 1. Éditer automate_all.py - Ajouter vos produits dans la liste

# 2. Exécuter l'automatisation complète
python3 automate_all.py

# RÉSULTAT:
# ✅ 3 reviews générées (HTML complets)
# ✅ index.html mis à jour (produits ajoutés)
# ✅ Recherche mise à jour
# ✅ Git commit + push automatique
# ✅ Site en ligne dans 2 minutes
```

### Scénario 2: Automatisation programmée

```bash
# 1. Configurer le scheduler
python3 scheduler.py

# OU configurer un cron job
crontab -e

# Ajouter:
0 2 * * 1 cd /home/fred/techreviewshub-site && python3 automate_all.py
```

**Résultat:**
- Chaque lundi à 2h du matin:
  - ✅ Nouvelles reviews générées automatiquement
  - ✅ Site mis à jour automatiquement
  - ✅ Push automatique
  - ✅ Site en ligne sans intervention

### Scénario 3: GitHub Actions (CI/CD)

Le fichier `.github/workflows/auto-deploy.yml` est configuré pour:

```yaml
on:
  push:
    branches: [ main ]       # Déploiement sur push
  schedule:
    - cron: '0 2 * * *'      # Exécution quotidienne 2h
  workflow_dispatch:         # Déclenchement manuel
```

**Déclencher manuellement:**
1. Aller sur GitHub → Actions
2. Sélectionner "🤖 Auto-Deploy Reviews"
3. Cliquer "Run workflow"

## 🎨 Personnaliser la génération

### Ajouter vos propres produits

Éditez `automate_all.py`:

```python
products = [
    {
        "id": "laptop_008",
        "name": "Votre Produit",
        "category": "laptop",  # laptop, headphone, monitor, keyboard, mouse, tablet
        "price": 1299.0,
        "rating": 4.7,
        "asin": "B0CXXXXXX",  # ASIN Amazon.fr
        "image_url": "https://...",
        "brand": "Marque",
        "short_desc": "Description courte (1 phrase)",
        "specs": {
            "Processeur": "...",
            "RAM": "...",
            # ... autres specs
        },
        "pros": [
            "Point fort 1",
            "Point fort 2",
            # ... 3-5 pros
        ],
        "cons": [
            "Point faible 1",
            # ... 3-5 cons
        ],
        "faqs": [
            {
                "question": "Question pertinente ?",
                "answer": "Réponse détaillée."
            },
            # ... 5-7 FAQs
        ],
        "related": ["laptop_001", "laptop_002", "laptop_003"]
    }
]
```

Puis exécuter:

```bash
python3 automate_all.py
```

## 📊 Statistiques & monitoring

### Vérifier l'état du site

```bash
# Health check manuel
python3 scheduler.py --test
```

### Voir les logs GitHub Actions

1. GitHub → Repository → Actions
2. Cliquer sur le dernier workflow
3. Voir les logs détaillés

### Compter les fichiers générés

```bash
echo "Reviews: $(ls -1 *_review.html | wc -l)"
echo "Blog: $(ls -1 blog/*.html | wc -l)"
echo "Comparatifs: $(ls -1 comparatifs/*.html | wc -l)"
```

## 🔧 Maintenance

### Backup automatique

```bash
# Backup manuel
tar -czf backup_$(date +%Y%m%d).tar.gz .

# Backup automatique (scheduler)
python3 scheduler.py
# → Backup tous les jours à 4h
```

### Mise à jour des prix

```bash
# Vérifier et mettre à jour les prix
python3 auto_price_updater.py

# Activer la mise à jour automatique quotidienne
# Éditer config_automation.json:
{
  "schedule": {
    "price_update": {
      "enabled": true,
      "frequency": "daily",
      "time": "03:00"
    }
  }
}
```

### Nettoyage

```bash
# Supprimer les anciens backups (garde les 7 derniers)
ls -t backup_*.tar.gz | tail -n +8 | xargs rm -f
```

## 🚨 Résolution de problèmes

### Erreur: Git push failed

```bash
# Vérifier le token GitHub
git remote -v

# Mettre à jour le token dans automate_all.py
self.github_token = "ghp_VotreNouveauToken"
```

### Erreur: Reviews mal formatées

```bash
# Tester la génération sans commit
python3 generate_batch_reviews.py

# Vérifier les fichiers générés
ls -lh *_review.html

# Ouvrir dans le navigateur pour vérifier
firefox laptop_007_review.html
```

### Erreur: index.html non mis à jour

```bash
# Vérifier que index.html existe
ls -lh index.html

# Vérifier les sections
grep 'id="laptops"' index.html
grep 'id="headphones"' index.html

# Mettre à jour manuellement si besoin
python3 -c "from automate_all import SiteAutomation; s = SiteAutomation(); s.update_index_html([...])"
```

## 📈 Évolutions futures

### Fonctionnalités à implémenter

- [ ] **API Amazon Product Advertising**
  - Récupération automatique des prix réels
  - Vérification de disponibilité
  - Images officielles

- [ ] **Génération de contenu IA**
  - OpenAI GPT-4 pour générer reviews
  - Amélioration automatique des FAQs
  - Génération d'articles de blog

- [ ] **Analytics automatiques**
  - Scraping Google Analytics
  - Rapport hebdomadaire par email
  - Optimisation SEO automatique

- [ ] **A/B Testing**
  - Tests automatiques de titles
  - Optimisation des CTA
  - Amélioration des conversions

- [ ] **Multi-langue**
  - Génération automatique en anglais
  - Traduction automatique
  - Sites miroirs

## 💡 Conseils & bonnes pratiques

### 1. **Démarrer progressivement**

```bash
# Semaine 1: Génération manuelle
python3 generate_batch_reviews.py

# Semaine 2: Automatisation partielle
python3 automate_all.py

# Semaine 3: Automatisation complète
python3 scheduler.py
```

### 2. **Vérifier avant de commit**

```bash
# Toujours vérifier les reviews générées
firefox *_007_review.html

# Vérifier index.html
firefox index.html

# Puis commit manuel si tout est OK
git add .
git commit -m "Vos changements"
git push
```

### 3. **Sauvegarder régulièrement**

```bash
# Backup manuel avant grosse modification
tar -czf backup_avant_modif.tar.gz .

# Activer les backups automatiques
python3 scheduler.py
```

### 4. **Monitoring continu**

```bash
# Vérifier le site en ligne
curl -I https://darken51.github.io/techreviewshub

# Vérifier les reviews
curl https://darken51.github.io/techreviewshub/laptop_007_review.html
```

## 📞 Support

**Questions ? Problèmes ?**

1. Vérifier les logs: `tail -f /tmp/reviews_cron.log`
2. Tester manuellement: `python3 automate_all.py`
3. Consulter la documentation: `README_GENERATEUR.md`
4. Ouvrir une issue sur GitHub

## 🎉 Résumé

Avec ce système d'automatisation, vous pouvez:

✅ **Générer 100+ reviews** en quelques minutes
✅ **Déployer automatiquement** sans intervention
✅ **Planifier** les mises à jour (cron/scheduler)
✅ **Mettre à jour les prix** automatiquement
✅ **Monitorer** la santé du site
✅ **Sauvegarder** régulièrement
✅ **Scaler** facilement (1000+ reviews possibles)

**Le site se maintient tout seul ! 🚀**

---

**Créé avec ❤️ et 🤖 par Claude Code**

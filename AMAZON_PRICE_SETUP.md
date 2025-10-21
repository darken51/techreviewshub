# Configuration Amazon Product Advertising API

Guide complet pour configurer l'update automatique des prix Amazon sur votre site.

---

## 📋 Prérequis

1. **Compte Amazon Associates actif** avec au moins 3 ventes qualifiées dans les 6 derniers mois
2. **Site web approuvé** par Amazon Associates (darken51.github.io/techreviewshub)
3. **Accès aux credentials API** (Access Key, Secret Key)

---

## 🚀 Étape 1 : Créer un compte Product Advertising API

### 1.1 S'inscrire à l'API

1. Rendez-vous sur : https://webservices.amazon.com/paapi5/signup
2. Connectez-vous avec votre compte Amazon Associates
3. Acceptez les conditions d'utilisation de l'API
4. Notez votre **Partner Tag** (ex: `techrevie06ac-21`)

### 1.2 Obtenir les credentials

1. Allez dans votre compte AWS : https://console.aws.amazon.com/
2. Cliquez sur votre nom en haut à droite → "Security credentials"
3. Créez un nouvel Access Key :
   - Type : "Application running outside AWS"
   - Description : "TechReviewsHub Price Updater"
4. **Téléchargez** et sauvegardez immédiatement :
   - **Access Key ID** (ex: `AKIAIOSFODNN7EXAMPLE`)
   - **Secret Access Key** (ex: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)

⚠️ **IMPORTANT** : La Secret Key n'est affichée qu'une seule fois. Sauvegardez-la immédiatement !

---

## 🔧 Étape 2 : Configurer le script Python

### 2.1 Créer le fichier de configuration

Créez un fichier `amazon_api_config.json` avec vos credentials :

```json
{
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "partner_tag": "techrevie06ac-21",
    "region": "eu-west-1"
}
```

⚠️ **Sécurité** : Ajoutez ce fichier à `.gitignore` pour ne jamais commiter vos credentials !

```bash
echo "amazon_api_config.json" >> .gitignore
```

### 2.2 Installer les dépendances Python

```bash
pip install python-amazon-paapi
```

Ou avec un virtual environment (recommandé) :

```bash
python3 -m venv venv
source venv/bin/activate
pip install python-amazon-paapi
```

---

## 🎯 Étape 3 : Utiliser le script

### 3.1 Update manuel des prix

Pour mettre à jour les prix de toutes les reviews :

```bash
python3 amazon_price_updater.py
```

Sortie attendue :
```
✅ API Amazon Product Advertising connectée
🚀 Mise à jour des prix pour 27 reviews...

📝 Vérification des prix pour laptop_001_review.html...
  → 1 ASIN(s) trouvé(s): B0CCKS8FVL
  Prix actuel dans le fichier : 1799.0€
  ✅ Nouveau prix trouvé : 1699.0€ (changement: -100.00€)

...

📊 Résumé de la mise à jour:
  ✅ Prix mis à jour : 12
  ℹ️  Prix inchangés : 15
  ⚠️  Erreurs : 0
```

### 3.2 Générer un log des prix (sans API)

Pour simplement logger les prix actuels sans les mettre à jour :

```bash
python3 amazon_price_updater.py --log
```

Ceci génère un fichier `price_history.log` avec tous les prix actuels.

---

## ⏰ Étape 4 : Automatiser avec Cron

### 4.1 Créer un script d'automation

Créez `update_prices_cron.sh` :

```bash
#!/bin/bash
cd /home/fred/techreviewshub-site
source venv/bin/activate  # Si vous utilisez un venv
python3 amazon_price_updater.py >> price_update.log 2>&1

# Si des prix ont été mis à jour, commit et push
if git diff --quiet; then
    echo "Aucun changement de prix"
else
    git add *_review.html price_history.log
    git commit -m "Update: Prix Amazon mis à jour automatiquement $(date +'%Y-%m-%d')"
    git push https://$GITHUB_TOKEN@github.com/darken51/techreviewshub.git main
fi
```

Rendez-le exécutable :

```bash
chmod +x update_prices_cron.sh
```

### 4.2 Configurer le Cron Job

Éditez votre crontab :

```bash
crontab -e
```

Ajoutez une ligne pour exécuter l'update **tous les lundis à 3h du matin** :

```bash
0 3 * * 1 /home/fred/techreviewshub-site/update_prices_cron.sh
```

Ou **tous les jours à 4h du matin** :

```bash
0 4 * * * /home/fred/techreviewshub-site/update_prices_cron.sh
```

### 4.3 Vérifier le Cron Job

Vérifiez que le cron est bien configuré :

```bash
crontab -l
```

Vérifiez les logs après la première exécution :

```bash
cat /home/fred/techreviewshub-site/price_update.log
```

---

## 📊 Étape 5 : Monitoring

### 5.1 Historique des prix

Le fichier `price_history.log` contient l'historique de tous les prix :

```
=== Vérification des prix - 2025-10-21 10:20:28 ===
laptop_001_review.html: B0CCKS8FVL = 1799.0€
laptop_002_review.html: B0CM65DBG5 = 1999.0€
...

=== Vérification des prix - 2025-10-28 10:20:15 ===
laptop_001_review.html: B0CCKS8FVL = 1699.0€  ← Prix baissé !
laptop_002_review.html: B0CM65DBG5 = 1999.0€
...
```

### 5.2 Dashboard des changements

Pour voir les changements de prix récents :

```bash
tail -100 price_history.log
```

Pour compter les mises à jour de prix :

```bash
git log --grep="Prix Amazon" --oneline | wc -l
```

---

## 🔐 Sécurité

### Fichiers à ne JAMAIS commiter

Ajoutez à `.gitignore` :

```
amazon_api_config.json
*.log
venv/
__pycache__/
```

### Protection du token GitHub

Si vous utilisez `update_prices_cron.sh`, définissez `GITHUB_TOKEN` comme variable d'environnement :

```bash
export GITHUB_TOKEN="ghp_VotreTokenIci"
```

Ou ajoutez-le à votre `~/.bashrc` / `~/.zshrc` :

```bash
echo 'export GITHUB_TOKEN="ghp_VotreTokenIci"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📈 Limites de l'API Amazon

- **Requests par seconde** : Max 1 req/sec (donc ~27 secondes pour 27 reviews)
- **Requests par jour** : Max 8,640 req/jour (largement suffisant)
- **Cache recommandé** : Cachez les résultats pendant 1h minimum
- **Respect des ToS** : Ne pas revendre les données, ne pas stocker les prix > 24h

Si vous dépassez les limites, l'API retournera une erreur `TooManyRequests`.

---

## 🐛 Troubleshooting

### Erreur : "InvalidClientTokenId"

→ Vérifiez que votre Access Key est correct dans `amazon_api_config.json`

### Erreur : "SignatureDoesNotMatch"

→ Vérifiez que votre Secret Key est correct

### Erreur : "The request signature we calculated does not match"

→ Vérifiez que votre région est correcte (`eu-west-1` pour Amazon.fr)

### Erreur : "You are not authorized to call this operation"

→ Votre compte Amazon Associates n'est pas encore approuvé pour l'API PA-API 5.0
→ Contactez le support Amazon Associates

### Aucun prix mis à jour

→ Vérifiez que les ASINs dans vos reviews sont corrects
→ Vérifiez que les produits sont toujours disponibles sur Amazon
→ Vérifiez les logs : `cat price_update.log`

---

## 📚 Ressources

- **Documentation officielle PA-API 5.0** : https://webservices.amazon.com/paapi5/documentation/
- **SDK Python** : https://github.com/sergioteula/python-amazon-paapi
- **Support Amazon Associates** : https://affiliate-program.amazon.fr/help
- **Limites de l'API** : https://webservices.amazon.com/paapi5/documentation/troubleshooting/api-rates.html

---

## ✅ Checklist de Configuration

- [ ] Compte Amazon Associates créé et approuvé
- [ ] 3+ ventes qualifiées dans les 6 derniers mois
- [ ] Inscrit à Product Advertising API 5.0
- [ ] Access Key et Secret Key récupérés
- [ ] Fichier `amazon_api_config.json` créé
- [ ] `amazon_api_config.json` ajouté à `.gitignore`
- [ ] SDK Python installé : `pip install python-amazon-paapi`
- [ ] Script testé : `python3 amazon_price_updater.py --log`
- [ ] Cron job configuré pour updates automatiques
- [ ] Monitoring configuré (`price_history.log`)

---

**Note** : Si vous n'avez pas encore accès à l'API PA-API 5.0, les prix resteront statiques mais seront toujours affichés avec la date de dernière vérification (21/10/2025) grâce aux améliorations SEO.

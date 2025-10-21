# 🤖 Générateur Automatique de Reviews Tech

Outil pour générer automatiquement des reviews HTML complètes suivant le même pattern que les 21 reviews existantes.

## ✨ Fonctionnalités

- ✅ **Structure HTML identique** aux reviews manuelles
- ✅ **SEO optimisé** : meta tags, Open Graph, Twitter Cards
- ✅ **Schema.org** : Product, Review, FAQPage markup
- ✅ **FAQ avec JavaScript** : collapsible, Schema.org compliant
- ✅ **Social sharing** : Facebook, Twitter, LinkedIn, WhatsApp, Email
- ✅ **Google Analytics** : tracking automatique
- ✅ **Responsive design** : mobile-first CSS
- ✅ **Amazon affiliate** : liens avec tag techrevie06ac-21

## 📦 Fichiers

- `generate_review_auto.py` : Générateur principal (classe ReviewGenerator)
- `generate_batch_reviews.py` : Script pour générer plusieurs reviews en batch
- `README_GENERATEUR.md` : Ce fichier

## 🚀 Utilisation

### Méthode 1 : Génération unitaire

```python
from generate_review_auto import ReviewGenerator

generator = ReviewGenerator()

product = {
    "id": "laptop_008",
    "name": "MSI Raider GE78",
    "category": "laptop",  # laptop, headphone, monitor, keyboard, mouse, tablet
    "price": 2599.0,
    "rating": 4.8,
    "asin": "B0CXXXXXXX",  # ASIN Amazon.fr
    "image_url": "https://...",
    "brand": "MSI",
    "short_desc": "Laptop gaming RTX 4090 avec écran Mini LED",
    "specs": {
        "Processeur": "Intel Core i9-13980HX",
        "GPU": "NVIDIA RTX 4090 16GB",
        # ... autres specs
    },
    "pros": [
        "RTX 4090 la plus puissante pour laptop",
        "Écran Mini LED 240Hz exceptionnel",
        # ... 3-5 points forts
    ],
    "cons": [
        "Prix très élevé (2599€)",
        "Poids 3.1kg",
        # ... 3-5 points faibles
    ],
    "faqs": [
        {
            "question": "Question pertinente sur le produit ?",
            "answer": "Réponse détaillée et utile pour l'utilisateur."
        },
        # ... 5-7 FAQs
    ],
    "related": ["laptop_007", "laptop_005", "laptop_003"]
}

filename, html = generator.generate_review(product)

# Sauvegarder
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Review créée : {filename}")
```

### Méthode 2 : Génération en batch

1. **Modifier `generate_batch_reviews.py`**
   - Ajoutez vos produits dans la liste `PRODUCTS_TO_GENERATE`

2. **Exécuter le script**
   ```bash
   python3 generate_batch_reviews.py
   ```

3. **Résultat**
   - Tous les fichiers HTML sont créés automatiquement
   - Prêts à déployer sur le site

## 📝 Structure des données produit

```python
{
    # OBLIGATOIRE
    "id": "category_XXX",           # Format: laptop_007, headphone_006, etc.
    "name": "Nom Complet Produit",  # Ex: "Sony WH-1000XM5"
    "category": "laptop",           # laptop, headphone, monitor, keyboard, mouse, tablet
    "price": 329.0,                 # Prix en euros (float)
    "rating": 4.8,                  # Note /5 (1.0 à 5.0)
    "asin": "B09Y2MYL5C",          # ASIN Amazon.fr (10 caractères)
    "image_url": "https://...",     # URL image produit (CDN fabricant)
    "brand": "Sony",                # Marque du produit
    "short_desc": "Description courte (1 phrase)",

    # Specs techniques (dictionnaire flexible)
    "specs": {
        "Clé1": "Valeur1",
        "Clé2": "Valeur2",
        # Adaptez selon la catégorie :
        # - Laptop: Processeur, GPU, RAM, Stockage, Écran, Autonomie, Poids
        # - Casque: Type, ANC, Autonomie, Connectivité, Codecs, Poids
        # - Moniteur: Taille, Résolution, Dalle, Fréquence, Temps réponse
        # - Clavier: Type switches, Layout, Connectivité, Autonomie, RGB
        # - Souris: Capteur, DPI, Connectivité, Autonomie, Poids, Boutons
        # - Tablette: Processeur, RAM, Stockage, Écran, Autonomie, OS
    },

    # Points forts (3-5 items)
    "pros": [
        "Point fort 1 spécifique et mesurable",
        "Point fort 2",
        "Point fort 3"
    ],

    # Points faibles (3-5 items)
    "cons": [
        "Point faible 1",
        "Point faible 2"
    ],

    # FAQs (5-7 questions)
    "faqs": [
        {
            "question": "Question pertinente et naturelle ?",
            "answer": "Réponse complète (2-4 phrases). Ajoutez des détails techniques, comparaisons, conseils pratiques."
        }
    ],

    # Produits similaires (3 IDs)
    "related": ["category_XXX", "category_YYY", "category_ZZZ"]
}
```

## 🎯 Bonnes pratiques FAQ

Les FAQs doivent répondre aux questions réelles des utilisateurs :

**Pour Laptops :**
- Gaming vs productivité ?
- Autonomie réelle ?
- Peut-on upgrader RAM/SSD ?
- Chauffe-t-il beaucoup ?
- Vaut-il son prix ?
- Quelle garantie ?

**Pour Casques :**
- Compatible iPhone/Android ?
- Autonomie réelle ?
- ANC efficace en avion/métro ?
- Confort pour longues sessions ?
- Vaut-il le prix vs concurrence ?
- Garantie ?

**Pour Moniteurs :**
- Compatible Mac/PC ?
- Bon pour gaming compétitif ?
- Fatigue oculaire ?
- Calibration nécessaire ?
- Vaut-il son prix ?
- Garantie pixel mort ?

**Pour Claviers :**
- Switches mécaniques vs membrane ?
- Compatible Mac/Windows/Linux ?
- Bon pour programmation ?
- Bruyant au bureau ?
- Autonomie sans fil ?
- Garantie ?

**Pour Souris :**
- DPI optimal pour gaming/bureautique ?
- Ergonomie (main droite/gauche, taille) ?
- Gaming vs productivité ?
- Autonomie batterie ?
- Vaut-il le prix ?
- Garantie ?

**Pour Tablettes :**
- Remplace-t-elle un laptop ?
- Clavier/stylet inclus ou séparé ?
- Stockage extensible (microSD) ?
- Bonne pour dessiner/noter ?
- Vaut-elle le prix ?
- Garantie ?

## 📊 Exemple complet de génération

```bash
# 1. Créer les reviews
python3 generate_batch_reviews.py

# 2. Vérifier les fichiers générés
ls -lh *_review.html

# 3. Tester en local
# Ouvrir laptop_007_review.html dans le navigateur

# 4. Ajouter au site
# Éditer index.html pour ajouter les nouveaux produits

# 5. Commit et push
git add .
git commit -m "Ajout de 3 nouvelles reviews auto-générées"
git push
```

## 🔧 Personnalisation

### Modifier le template CSS

Éditez `ReviewGenerator._generate_html()` dans `generate_review_auto.py` :

```python
# Ligne ~400: styles CSS
body {{
    font-family: 'Votre-Font', sans-serif;
    # ... vos styles
}}
```

### Ajouter des sections

Ajoutez du HTML dans la méthode `_generate_html()` :

```python
# Après la section FAQ
<div class="custom-section">
    <h2>Ma Section Personnalisée</h2>
    <p>Contenu...</p>
</div>
```

### Changer le tag affilié

Remplacez `techrevie06ac-21` dans le code :

```python
# Ligne ~60 et suivantes
"url": "https://amazon.fr/dp/{p["asin"]}?tag=VOTRE-TAG-21"
```

## 📈 Statistiques

Avec ce générateur, vous pouvez :

- ✅ Générer **1 review** en **< 1 seconde**
- ✅ Générer **10 reviews** en **< 5 secondes**
- ✅ Générer **100 reviews** en **< 1 minute**

Chaque review contient :
- **~27,000 caractères** (~3,800 mots)
- **6-7 FAQs** Schema.org compliant
- **SEO complet** (meta tags, OG, Twitter, Schema)
- **JavaScript interactif** (FAQ toggle, social sharing)
- **Google Analytics** tracking

## ❓ FAQ du générateur

**Q : Les reviews générées sont-elles SEO-friendly ?**
R : Oui, structure identique aux reviews manuelles : meta tags, Schema.org, FAQPage, canonical URLs.

**Q : Puis-je modifier le HTML après génération ?**
R : Oui, les fichiers HTML peuvent être édités manuellement pour personnalisation.

**Q : Comment trouver l'ASIN Amazon ?**
R : Sur la page produit Amazon.fr, l'ASIN est dans l'URL ou dans "Détails du produit" (code à 10 caractères).

**Q : Les images sont-elles hébergées ?**
R : Non, utilisez des URLs d'images officielles des fabricants (CDN). Pas de téléchargement.

**Q : Le générateur supporte-t-il d'autres langues ?**
R : Non, actuellement français seulement. Facile à adapter en modifiant les templates.

**Q : Peut-on générer des comparatifs ou guides ?**
R : Non, seulement des reviews produits. Comparatifs et guides nécessitent un template différent.

## 🚀 Prochaines étapes

1. ✅ Créez votre première review avec `generate_review_auto.py`
2. ✅ Testez en local dans le navigateur
3. ✅ Générez plusieurs reviews avec `generate_batch_reviews.py`
4. ✅ Ajoutez-les à `index.html` (section catégorie appropriée)
5. ✅ Commit et push vers GitHub
6. ✅ Site automatiquement déployé sur GitHub Pages !

## 💡 Conseils

- **Qualité des FAQs** : Posez-vous "Qu'est-ce que mes lecteurs vont vraiment chercher sur Google ?"
- **Images** : Préférez les CDN officiels (Lenovo, Sony, etc.) pour images haute qualité
- **ASIN** : Vérifiez toujours que l'ASIN est correct et pointe vers Amazon.fr (pas .com)
- **Specs** : Soyez précis et mesurables ("32 GB DDR5-5600" au lieu de "Beaucoup de RAM")
- **Prix** : Vérifiez le prix actuel sur Amazon.fr avant de générer

## 📞 Support

Questions ? Problèmes ? Idées d'amélioration ?

- Ouvrez une issue sur GitHub
- Ou contactez directement l'équipe Tech Reviews Hub

---

**Happy generating! 🎉**

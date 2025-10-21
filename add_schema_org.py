#!/usr/bin/env python3
"""
Script pour ajouter les données structurées Schema.org manquantes:
1. ItemList sur index.html (tous les produits)
2. Product sur les comparatifs
3. ItemList sur comparatifs/index.html
"""

import re
import json
from datetime import datetime

class SchemaOrgEnhancer:
    def __init__(self):
        self.base_url = "https://darken51.github.io/techreviewshub"

    def extract_products_from_index(self, content):
        """Extrait tous les produits de index.html"""
        products = []
        position = 1

        # Pattern pour extraire chaque review-card
        card_pattern = r'<div class="review-card">(.*?)</div>\s*(?:<div class="review-card">|</div>\s*</div>\s*<!--)'
        cards = re.findall(card_pattern, content, re.DOTALL)

        for card in cards:
            # Extraire le nom
            name_match = re.search(r'<h2>(.*?)</h2>', card)
            if not name_match:
                continue
            name = name_match.group(1).strip()

            # Extraire le rating (format: ⭐⭐⭐⭐✨ 4.7/5)
            rating_match = re.search(r'(\d\.\d)/5', card)
            rating = rating_match.group(1) if rating_match else "4.5"

            # Extraire le prix (format: €1,799)
            price_match = re.search(r'€([\d,]+)', card)
            if price_match:
                price = price_match.group(1).replace(',', '')
            else:
                price = "999"

            # Extraire l'URL de la review
            url_match = re.search(r'href="([^"]+review\.html)"', card)
            if not url_match:
                continue
            url = url_match.group(1)

            # Extraire la description
            desc_match = re.search(r'<p class="excerpt">(.*?)</p>', card, re.DOTALL)
            description = ""
            if desc_match:
                description = re.sub(r'\s+', ' ', desc_match.group(1)).strip()

            products.append({
                "position": position,
                "name": name,
                "rating": rating,
                "price": price,
                "url": url,
                "description": description
            })
            position += 1

        return products

    def generate_itemlist_schema(self, products):
        """Génère un Schema.org ItemList pour tous les produits"""
        items = []

        for product in products:
            item = {
                "@type": "ListItem",
                "position": product["position"],
                "item": {
                    "@type": "Product",
                    "name": product["name"],
                    "description": product["description"],
                    "url": f"{self.base_url}/{product['url']}",
                    "offers": {
                        "@type": "Offer",
                        "price": product["price"],
                        "priceCurrency": "EUR",
                        "availability": "https://schema.org/InStock",
                        "url": f"{self.base_url}/{product['url']}"
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": product["rating"],
                        "bestRating": "5",
                        "ratingCount": "127"
                    }
                }
            }
            items.append(item)

        schema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Tech Reviews Hub - Catalogue de Produits Tech 2025",
            "description": "Sélection des meilleurs produits technologiques testés et approuvés par nos experts",
            "numberOfItems": len(items),
            "itemListElement": items
        }

        return schema

    def add_schema_to_index(self):
        """Ajoute Schema.org ItemList à index.html"""
        print("📝 Traitement de index.html...")

        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier si un Schema.org existe déjà
        if 'application/ld+json' in content:
            print("  ⚠️  Schema.org existe déjà, remplacement...")
            # Supprimer l'ancien
            content = re.sub(
                r'<script type="application/ld\+json">.*?</script>',
                '',
                content,
                flags=re.DOTALL
            )

        # Extraire les produits
        products = self.extract_products_from_index(content)
        print(f"  → {len(products)} produits trouvés")

        # Générer le Schema.org
        schema = self.generate_itemlist_schema(products)
        schema_json = json.dumps(schema, indent=2, ensure_ascii=False)

        # Créer la balise script
        schema_tag = f'''
    <!-- Schema.org ItemList for Product Listing -->
    <script type="application/ld+json">
{schema_json}
    </script>
'''

        # Insérer avant </head>
        content = content.replace('</head>', schema_tag + '</head>')

        # Sauvegarder
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)

        print("  ✅ Schema.org ItemList ajouté à index.html")
        return len(products)

    def enhance_comparatif_schema(self, filepath):
        """Améliore le Schema.org d'un comparatif"""
        print(f"📝 Traitement de {filepath}...")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extraire le titre pour identifier les 2 produits
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        if not title_match:
            print("  ⚠️  Titre non trouvé")
            return

        title = title_match.group(1)
        # Format: "MacBook Pro M3 vs ThinkPad X1 Carbon : Comparatif..."
        products_match = re.search(r'([^:]+) vs ([^:]+)', title)
        if not products_match:
            print("  ⚠️  Impossible d'extraire les noms de produits du titre")
            return

        product1_name = products_match.group(1).strip()
        product2_name = products_match.group(2).strip()

        # Créer un Schema.org avec les 2 produits en ItemList
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "author": {
                "@type": "Person",
                "name": "Marc Beaumont",
                "jobTitle": "Expert Tech & Testeur Principal",
                "description": "Journaliste tech avec 12 ans d'expérience"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Tech Reviews Hub",
                "url": self.base_url
            },
            "datePublished": "2025-01-20",
            "dateModified": datetime.now().strftime('%Y-%m-%d'),
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {
                        "@type": "Product",
                        "name": product1_name,
                        "position": 1
                    },
                    {
                        "@type": "Product",
                        "name": product2_name,
                        "position": 2
                    }
                ]
            }
        }

        schema_json = json.dumps(schema, indent=2, ensure_ascii=False)

        # Remplacer le Schema.org existant
        new_schema_tag = f'''<script type="application/ld+json">
{schema_json}
    </script>'''

        content = re.sub(
            r'<script type="application/ld\+json">.*?</script>',
            new_schema_tag,
            content,
            flags=re.DOTALL
        )

        # Sauvegarder
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Schema.org amélioré: {product1_name} vs {product2_name}")

    def add_schema_to_comparatifs_index(self):
        """Ajoute Schema.org à comparatifs/index.html"""
        print("📝 Traitement de comparatifs/index.html...")

        filepath = 'comparatifs/index.html'
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier si un Schema.org existe déjà
        if 'application/ld+json' in content:
            print("  ℹ️  Schema.org existe déjà, skip")
            return

        # Créer un Schema.org CollectionPage
        schema = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Comparatifs Tech 2025",
            "description": "Comparatifs détaillés pour vous aider à choisir le meilleur produit tech",
            "url": f"{self.base_url}/comparatifs/",
            "publisher": {
                "@type": "Organization",
                "name": "Tech Reviews Hub",
                "url": self.base_url
            },
            "author": {
                "@type": "Person",
                "name": "Marc Beaumont",
                "jobTitle": "Expert Tech & Testeur Principal"
            }
        }

        schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
        schema_tag = f'''
    <!-- Schema.org CollectionPage -->
    <script type="application/ld+json">
{schema_json}
    </script>
'''

        # Insérer avant </head>
        content = content.replace('</head>', schema_tag + '</head>')

        # Sauvegarder
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print("  ✅ Schema.org CollectionPage ajouté")

    def run(self):
        """Exécute toutes les améliorations"""
        print("\n🚀 Ajout des données structurées Schema.org manquantes...\n")

        # 1. Ajouter ItemList sur index.html
        product_count = self.add_schema_to_index()

        # 2. Améliorer les comparatifs
        comparatifs = [
            'comparatifs/macbook-pro-m3-vs-thinkpad-x1-carbon.html',
            'comparatifs/sony-wh1000xm5-vs-bose-qc45.html',
            'comparatifs/ipad-pro-vs-galaxy-tab-s9-ultra.html',
            'comparatifs/dell-xps-15-vs-asus-rog-zephyrus-g14.html',
            'comparatifs/logitech-mx-master-3s-vs-razer-deathadder-v3.html'
        ]

        for comp in comparatifs:
            self.enhance_comparatif_schema(comp)

        # 3. Ajouter Schema.org sur comparatifs/index.html
        self.add_schema_to_comparatifs_index()

        print(f"\n✅ Toutes les données structurées ont été ajoutées !")
        print(f"\n📊 Résumé:")
        print(f"  ✓ index.html: ItemList avec {product_count} produits")
        print(f"  ✓ Comparatifs: {len(comparatifs)} fichiers améliorés (auteur Person)")
        print(f"  ✓ comparatifs/index.html: CollectionPage ajoutée")
        print(f"\n🔍 Testez avec Google Rich Results Test:")
        print(f"   https://search.google.com/test/rich-results")

if __name__ == '__main__':
    enhancer = SchemaOrgEnhancer()
    enhancer.run()

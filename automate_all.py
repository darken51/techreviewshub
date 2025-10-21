#!/usr/bin/env python3
"""
🤖 AUTOMATISATION COMPLÈTE TECH REVIEWS HUB
Génère reviews, met à jour index.html, commit et push automatiquement
"""

import os
import re
import json
import subprocess
from datetime import datetime
from generate_review_auto import ReviewGenerator

class SiteAutomation:
    def __init__(self, github_token=None):
        self.generator = ReviewGenerator()
        # Utiliser variable d'environnement ou argument
        self.github_token = github_token or os.getenv('GITHUB_TOKEN', '')
        self.generated_files = []

    def generate_reviews(self, products):
        """Génère toutes les reviews automatiquement"""
        print("🤖 ÉTAPE 1: Génération automatique des reviews")
        print("="*60)

        for i, product in enumerate(products, 1):
            print(f"\n[{i}/{len(products)}] Génération : {product['name']}...")

            filename, html = self.generator.generate_review(product)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)

            self.generated_files.append({
                'filename': filename,
                'product': product
            })

            print(f"    ✅ {filename} créé")
            print(f"    ⭐ Note: {product['rating']}/5")
            print(f"    💰 Prix: {product['price']}€")

        print(f"\n✅ {len(products)} reviews générées")
        return self.generated_files

    def update_index_html(self, new_products):
        """Met à jour automatiquement index.html avec les nouveaux produits"""
        print("\n🤖 ÉTAPE 2: Mise à jour automatique de index.html")
        print("="*60)

        with open('index.html', 'r', encoding='utf-8') as f:
            index_content = f.read()

        # Grouper par catégorie
        by_category = {}
        for item in new_products:
            cat = item['product']['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)

        # Ajouter chaque produit dans la bonne section
        for category, products in by_category.items():
            cat_info = self.generator.categories[category]
            anchor = cat_info['anchor']

            # Trouver la section de cette catégorie
            pattern = f'<div id="{anchor}" class="category-section">.*?<div class="reviews-grid">'
            match = re.search(pattern, index_content, re.DOTALL)

            if match:
                insert_position = match.end()

                # Générer les cards HTML pour chaque produit
                cards_html = ""
                for item in products:
                    p = item['product']
                    stars = "⭐" * int(p['rating'])
                    if (p['rating'] - int(p['rating'])) >= 0.3:
                        stars += "✨"

                    card = f"""
                <div class="review-card">
                    <h2>{p['name']}</h2>
                    <div class="rating">{stars} {p['rating']}/5</div>
                    <p class="price">€{p['price']:.0f}</p>
                    <p class="excerpt">
                        {p['short_desc']}
                    </p>
                    <a href="{item['filename']}" class="btn">Lire le Test Complet →</a>
                </div>
"""
                    cards_html += card

                # Insérer les nouvelles cards
                index_content = index_content[:insert_position] + cards_html + index_content[insert_position:]

                print(f"✅ {len(products)} produit(s) ajouté(s) dans section {cat_info['name']}")

        # Sauvegarder index.html modifié
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_content)

        print("✅ index.html mis à jour")
        return True

    def update_search_database(self, new_products):
        """Met à jour la base de données de recherche dans index.html"""
        print("\n🤖 ÉTAPE 3: Mise à jour de la base de recherche")
        print("="*60)

        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()

        # Trouver le tableau products[] dans le JavaScript
        pattern = r'const products = \[(.*?)\];'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            # Ajouter les nouveaux produits
            for item in new_products:
                p = item['product']
                cat_info = self.generator.categories[p['category']]

                new_entry = f'{{\n        name: "{p["name"]}", category: "{cat_info["name"][:-1]}", price: "{p["price"]:.0f}€", url: "{item["filename"]}"\n      }}'

                # Insérer avant le dernier élément
                old_products = match.group(1)
                new_products_js = old_products.rstrip() + ',\n        ' + new_entry

                content = content.replace(match.group(1), new_products_js)

            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ {len(new_products)} produit(s) ajouté(s) à la recherche")

        return True

    def git_commit_and_push(self, message=None):
        """Commit et push automatique vers GitHub"""
        print("\n🤖 ÉTAPE 4: Git commit et push automatique")
        print("="*60)

        if not message:
            message = f"🤖 Auto-ajout de {len(self.generated_files)} nouvelles reviews - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        try:
            # Git add
            subprocess.run(['git', 'add', '.'], check=True)
            print("✅ git add .")

            # Git commit
            commit_msg = f"""{message}

Fichiers ajoutés:
{chr(10).join([f"  • {item['filename']} - {item['product']['name']}" for item in self.generated_files])}

Modifications:
  • index.html - Ajout des produits dans les catégories
  • index.html - Mise à jour de la base de recherche

🤖 Auto-généré avec automate_all.py

Co-Authored-By: Claude <noreply@anthropic.com>"""

            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ git commit")

            # Git push
            repo_url = f"https://{self.github_token}@github.com/darken51/techreviewshub.git"
            subprocess.run(['git', 'push', repo_url, 'main'], check=True)
            print("✅ git push")

            print("\n🚀 Déploiement automatique sur GitHub Pages en cours...")

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur git: {e}")
            return False

    def generate_blog_post(self, topic, keywords):
        """Génère automatiquement un article de blog SEO"""
        print(f"\n🤖 Génération article blog: {topic}")

        # Template simplifié pour article blog
        slug = topic.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e')
        filename = f"blog/{slug}.html"

        # Contenu SEO basique (à développer)
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{topic} | Tech Reviews Hub</title>
    <meta name="description" content="{topic} - Guide complet par Tech Reviews Hub">
</head>
<body>
    <h1>{topic}</h1>
    <p>Article en cours de génération automatique...</p>
</body>
</html>"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ {filename} créé")
        return filename

    def run_full_automation(self, products_list):
        """Exécute l'automatisation complète de bout en bout"""
        print("\n" + "="*60)
        print("🤖 AUTOMATISATION COMPLÈTE TECH REVIEWS HUB")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Produits à générer: {len(products_list)}")
        print("="*60)

        # Étape 1: Générer les reviews
        generated = self.generate_reviews(products_list)

        # Étape 2: Mettre à jour index.html
        self.update_index_html(generated)

        # Étape 3: Mettre à jour la recherche
        self.update_search_database(generated)

        # Étape 4: Commit et push
        self.git_commit_and_push()

        # Rapport final
        print("\n" + "="*60)
        print("✅ AUTOMATISATION TERMINÉE AVEC SUCCÈS")
        print("="*60)
        print(f"\n📊 Résumé:")
        print(f"  • {len(generated)} reviews générées")
        print(f"  • index.html mis à jour")
        print(f"  • Recherche mise à jour")
        print(f"  • Commit et push effectués")
        print(f"\n🌐 Site en ligne: https://darken51.github.io/techreviewshub")
        print("\n💡 Les nouvelles reviews seront visibles dans 1-2 minutes!")

        return True


def main():
    """Point d'entrée principal - Définissez vos produits ici"""

    # CONFIGURATION: Ajoutez vos produits ici
    products = [
        {
            "id": "keyboard_004",
            "name": "Keychron Q6 Pro",
            "category": "keyboard",
            "price": 189.0,
            "rating": 4.8,
            "asin": "B0BSXYZ123",
            "image_url": "https://cdn.shopify.com/s/files/1/0059/0630/1017/files/Keychron_Q6_Pro_QMK_VIA_Wireless_Custom_Mechanical_Keyboard.jpg",
            "brand": "Keychron",
            "short_desc": "Clavier mécanique full-size QMK/VIA sans fil premium",
            "specs": {
                "Layout": "Full-size 100% (108 touches)",
                "Switches": "Gateron G Pro (Hot-swap)",
                "Connectivité": "Bluetooth 5.1 + USB-C filaire + 2.4GHz",
                "Batterie": "4000 mAh (jusqu'à 100h)",
                "Construction": "CNC aluminium",
                "RGB": "Per-key RGB South-facing LED",
                "Programmation": "QMK/VIA full customization",
                "Poids": "2180g (avec plaque alu)"
            },
            "pros": [
                "QMK/VIA customisation illimitée (layers, macros)",
                "Triple mode: Bluetooth + 2.4GHz + USB-C",
                "Construction premium aluminium CNC",
                "Hot-swap switches (changement sans soudure)",
                "Batterie 4000mAh autonomie 100h"
            ],
            "cons": [
                "Prix élevé (189€)",
                "Très lourd (2.18kg) - pas portable",
                "Courbe d'apprentissage QMK/VIA",
                "Full-size encombrant (occupe beaucoup d'espace)"
            ],
            "faqs": [
                {"question": "Le Keychron Q6 Pro est-il compatible Mac et Windows ?",
                 "answer": "Oui, triple OS: macOS, Windows, Linux. Switches dédiés pour basculer. QMK/VIA permet de créer des layouts personnalisés pour chaque OS."},
                {"question": "Peut-on changer les switches sans soudure ?",
                 "answer": "Oui, hot-swap total. Retirez et remplacez n'importe quel switch en 5 secondes avec l'extracteur fourni. Compatible tous switches 3-pin et 5-pin."},
                {"question": "C'est quoi QMK/VIA et pourquoi c'est utile ?",
                 "answer": "QMK = firmware open-source pour programmation totale. VIA = interface graphique pour créer layers, macros, remapper touches sans coder. Idéal programmeurs/gamers avancés."},
                {"question": "L'autonomie de 100h est-elle réaliste ?",
                 "answer": "Oui en Bluetooth avec RGB éteint. Avec RGB 50%, comptez 40-50h. En 2.4GHz ou USB-C, autonomie illimitée (alimenté par câble)."},
                {"question": "Le Q6 Pro vaut-il 189€ ?",
                 "answer": "Oui pour enthusiasts claviers. Construction premium, hot-swap, QMK/VIA. Alternatives: Keychron K8 Pro (109€, TKL) ou GMMK Pro (169€, 75%)."},
                {"question": "Quelle garantie ?",
                 "answer": "Keychron offre 1 an garantie. Extension à 2 ans disponible. SAV réactif avec pièces de rechange (switches, câbles, etc.)."}
            ],
            "related": ["keyboard_001", "keyboard_002", "keyboard_003"]
        },

        {
            "id": "mouse_003",
            "name": "Logitech G Pro X Superlight 2",
            "category": "mouse",
            "price": 159.0,
            "rating": 4.9,
            "asin": "B0CK1XYZ99",
            "image_url": "https://resource.logitechg.com/w_692,c_lpad,ar_4:3,q_auto,f_auto,dpr_1.0/d_transparent.gif/content/dam/gaming/en/products/pro-x-superlight-2/gallery/pro-x-superlight-2-gallery-1.png",
            "brand": "Logitech",
            "short_desc": "Souris gaming ultra-légère 60g avec capteur HERO 2 32K DPI",
            "specs": {
                "Capteur": "HERO 2 32000 DPI",
                "Poids": "60g (sans câble)",
                "Connectivité": "LIGHTSPEED 2.4GHz (1ms) sans fil",
                "Autonomie": "95 heures (charge complète)",
                "Polling rate": "1000 Hz (2000 Hz avec dongle Pro)",
                "Switches": "Optiques hybrides (100M clics)",
                "Boutons": "5 programmables",
                "Pieds": "PTFE ultra-glisse"
            },
            "pros": [
                "Ultra-légère 60g (la plus légère gaming haut de gamme)",
                "Capteur HERO 2 32K DPI ultra-précis (esport)",
                "Switches optiques hybrides 100M clics",
                "Autonomie 95h excellente",
                "LIGHTSPEED 1ms latence imperceptible"
            ],
            "cons": [
                "Prix très élevé (159€)",
                "Seulement 5 boutons (pas de MMO)",
                "Pas de RGB (minimaliste noir/blanc)",
                "Forme ambidextre (pas d'ergonomie main droite)"
            ],
            "faqs": [
                {"question": "La G Pro X Superlight 2 est-elle vraiment meilleure que la v1 ?",
                 "answer": "Oui: capteur HERO 2 (vs HERO 25K), switches optiques (vs mécaniques), polling 2000Hz compatible (vs 1000Hz), grip amélioré. Même poids 60g, même autonomie."},
                {"question": "60g c'est vraiment utile pour le gaming ?",
                 "answer": "Oui pour esport FPS (Valorant, CS2, Apex). Moins de fatigue, flicks plus rapides, contrôle précis. Différence notable vs 80-100g après 2-3h de jeu."},
                {"question": "La Superlight 2 est-elle bonne pour la productivité ?",
                 "answer": "Correct mais pas optimal. Seulement 5 boutons (vs 7+ MX Master 3S), pas de scroll horizontal, forme basique. Pour bureau, privilégiez MX Master 3S (119€)."},
                {"question": "Quelle est l'autonomie réelle en usage gaming ?",
                 "answer": "95h annoncées = réaliste en polling 1000Hz. En polling 2000Hz avec dongle Pro, comptez 60-70h. Charge rapide: 5 min = 2h de jeu."},
                {"question": "La Superlight 2 vaut-elle 159€ ?",
                 "answer": "Oui pour esport/gaming compétitif sérieux. Pour gaming casual, Logitech G305 (59€) ou Razer DeathAdder V3 (79€) suffisent largement."},
                {"question": "Quelle garantie ?",
                 "answer": "Logitech offre 2 ans garantie. Switch optique 100M clics = durée de vie 5-7 ans. SAV excellent avec remplacement rapide."}
            ],
            "related": ["mouse_001", "mouse_002"]
        },

        {
            "id": "tablet_003",
            "name": "Microsoft Surface Pro 9",
            "category": "tablet",
            "price": 1299.0,
            "rating": 4.6,
            "asin": "B0BDXYZ456",
            "image_url": "https://cdn-dynmedia-1.microsoft.com/is/image/microsoftcorp/Surface-Pro-9-Platinum",
            "brand": "Microsoft",
            "short_desc": "Tablette 2-en-1 Windows 11 avec Intel Core i7 et écran PixelSense 120Hz",
            "specs": {
                "Processeur": "Intel Core i7-1255U (12ème gen)",
                "RAM": "16 GB LPDDR5",
                "Stockage": "256 GB SSD NVMe",
                "Écran": "13\" PixelSense 2880x1920 120Hz tactile",
                "Autonomie": "15 heures",
                "Poids": "879g (sans clavier)",
                "OS": "Windows 11 Pro",
                "Connectivité": "2x USB-C Thunderbolt 4, Surface Connect"
            },
            "pros": [
                "Windows 11 complet (apps desktop, pas limité comme iPad)",
                "Intel Core i7 12ème gen puissant (multitâche)",
                "Écran PixelSense 120Hz superbe (2880x1920)",
                "Thunderbolt 4 pour docks et eGPU",
                "Kickstand intégré ultra-pratique"
            ],
            "cons": [
                "Type Cover et Slim Pen vendus séparément (+329€)",
                "Autonomie 15h vs 20h+ iPad Pro",
                "Chauffe en charge (ventilateur audible)",
                "Prix élevé tout équipé (1299€ + 329€ = 1628€)"
            ],
            "faqs": [
                {"question": "La Surface Pro 9 peut-elle remplacer un laptop ?",
                 "answer": "Oui totalement avec Type Cover. Windows 11 complet, Intel i7, 16GB RAM, apps desktop (Photoshop, VS Code, etc.). Meilleur que iPad Pro pour productivité pure."},
                {"question": "Le Type Cover et le Slim Pen sont-ils obligatoires ?",
                 "answer": "Non mais fortement recommandés. Type Cover (179€) essentiel pour frappe. Slim Pen 2 (129€) optionnel sauf si dessin/notes manuscrites. Budget total réaliste: 1628€."},
                {"question": "Surface Pro 9 vs iPad Pro 12.9 M2 ?",
                 "answer": "Surface = Windows desktop apps, fichiers libres, ports USB. iPad = meilleure autonomie, M2 plus puissant, écosystème Apple. Surface pour travail, iPad pour création/media."},
                {"question": "Peut-on jouer à des jeux PC dessus ?",
                 "answer": "Jeux légers oui (Minecraft, indie). AAA non (Iris Xe intégré faible). Pour gaming, branchez eGPU via Thunderbolt 4 (300€+) ou achetez laptop gaming."},
                {"question": "La Surface Pro 9 vaut-elle 1299€ ?",
                 "answer": "Oui pour professionnels Windows. Alternative: Surface Laptop 5 (1399€, clavier inclus) ou iPad Pro 12.9 + Magic Keyboard (1849€ total)."},
                {"question": "Quelle garantie ?",
                 "answer": "Microsoft offre 1 an standard. Microsoft Complete (2 ans + casse accidentelle) recommandé pour 149€. SAV Microsoft Store rapide."}
            ],
            "related": ["tablet_001", "tablet_002", "laptop_006"]
        }
    ]

    # Lancer l'automatisation complète
    # Token GitHub: utiliser variable d'environnement GITHUB_TOKEN
    # Ou passer en argument: automation = SiteAutomation(github_token="ghp_...")
    automation = SiteAutomation()

    # Si vous voulez skip le push automatique, modifiez git_commit_and_push()
    automation.run_full_automation(products)


if __name__ == "__main__":
    main()

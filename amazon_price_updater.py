#!/usr/bin/env python3
"""
Amazon Price Updater - Met à jour automatiquement les prix des produits depuis Amazon.
Utilise l'API Amazon Product Advertising 5.0.

Configuration requise:
1. Créer un compte Amazon Associates : https://partenaires.amazon.fr/
2. S'inscrire à Product Advertising API : https://webservices.amazon.com/paapi5/signup
3. Obtenir les credentials : Access Key, Secret Key, Partner Tag
4. Créer un fichier amazon_api_config.json avec les credentials

Format amazon_api_config.json:
{
    "access_key": "VOTRE_ACCESS_KEY",
    "secret_key": "VOTRE_SECRET_KEY",
    "partner_tag": "techrevie06ac-21",
    "region": "eu-west-1"
}

Installation des dépendances:
pip install python-amazon-paapi
"""

import os
import re
import json
from datetime import datetime

# Configuration
CONFIG_FILE = 'amazon_api_config.json'
ASIN_PATTERN = r'amazon\.fr/dp/([A-Z0-9]{10})'
PRICE_PATTERN = r'"price":\s*"(\d+\.?\d*)"'

class AmazonPriceUpdater:
    def __init__(self, config_file=CONFIG_FILE):
        self.config = self.load_config(config_file)
        self.api_available = False
        self.amazon_api = None

        # Tenter d'initialiser l'API
        if self.config:
            try:
                from paapi5_python_sdk.api.default_api import DefaultApi
                from paapi5_python_sdk.partner_type import PartnerType
                from paapi5_python_sdk.rest import ApiException
                from paapi5_python_sdk.get_items_request import GetItemsRequest
                from paapi5_python_sdk.get_items_resource import GetItemsResource

                self.amazon_api = DefaultApi(
                    access_key=self.config['access_key'],
                    secret_key=self.config['secret_key'],
                    host='webservices.amazon.fr',
                    region=self.config.get('region', 'eu-west-1')
                )
                self.partner_tag = self.config['partner_tag']
                self.api_available = True
                print("✅ API Amazon Product Advertising connectée")
            except ImportError:
                print("⚠️  Module 'paapi5-python-sdk' non installé")
                print("   Installation : pip install python-amazon-paapi")
            except Exception as e:
                print(f"⚠️  Erreur connexion API Amazon: {e}")

    def load_config(self, config_file):
        """Charge la configuration API depuis le fichier JSON"""
        if not os.path.exists(config_file):
            print(f"⚠️  Fichier de configuration {config_file} non trouvé")
            print(f"   Créez le fichier avec vos credentials Amazon PA-API")
            return None

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError:
            print(f"❌ Erreur de parsing du fichier {config_file}")
            return None

    def get_price_from_api(self, asin):
        """Récupère le prix actuel depuis l'API Amazon"""
        if not self.api_available:
            return None

        try:
            from paapi5_python_sdk.get_items_request import GetItemsRequest
            from paapi5_python_sdk.get_items_resource import GetItemsResource
            from paapi5_python_sdk.partner_type import PartnerType

            get_items_request = GetItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace='www.amazon.fr',
                item_ids=[asin],
                resources=[
                    GetItemsResource.OFFERS_LISTINGS_PRICE
                ]
            )

            response = self.amazon_api.get_items(get_items_request)

            if response.items_result and response.items_result.items:
                item = response.items_result.items[0]
                if item.offers and item.offers.listings:
                    price = item.offers.listings[0].price.amount
                    return float(price)

            return None

        except Exception as e:
            print(f"  ⚠️  Erreur API pour ASIN {asin}: {e}")
            return None

    def extract_asins_from_file(self, filepath):
        """Extrait tous les ASINs d'un fichier HTML"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        asins = re.findall(ASIN_PATTERN, content)
        return list(set(asins))  # Dédoublonner

    def update_price_in_file(self, filepath, old_price, new_price):
        """Met à jour le prix dans un fichier HTML"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Mettre à jour le prix dans le Schema.org
        old_price_str = f'"price": "{old_price}"'
        new_price_str = f'"price": "{new_price}"'
        content = content.replace(old_price_str, new_price_str)

        # Mettre à jour le prix affiché dans le HTML
        # Format : <p class="price">1799€</p>
        old_display = f'<p class="price">{int(old_price)}€</p>'
        new_display = f'<p class="price">{int(new_price)}€</p>'
        content = content.replace(old_display, new_display)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def update_review_prices(self, filepath):
        """Met à jour les prix d'un fichier review"""
        print(f"📝 Vérification des prix pour {filepath}...")

        # Extraire les ASINs
        asins = self.extract_asins_from_file(filepath)
        if not asins:
            print(f"  ⚠️  Aucun ASIN trouvé")
            return

        print(f"  → {len(asins)} ASIN(s) trouvé(s): {', '.join(asins)}")

        # Extraire le prix actuel du fichier
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        price_match = re.search(PRICE_PATTERN, content)
        if not price_match:
            print(f"  ⚠️  Prix actuel non trouvé dans le fichier")
            return

        current_price = float(price_match.group(1))
        print(f"  Prix actuel dans le fichier : {current_price}€")

        # Récupérer le nouveau prix
        if self.api_available:
            new_price = self.get_price_from_api(asins[0])
            if new_price and abs(new_price - current_price) > 0.01:
                print(f"  ✅ Nouveau prix trouvé : {new_price}€ (changement: {new_price - current_price:+.2f}€)")
                self.update_price_in_file(filepath, current_price, new_price)
                return True
            elif new_price:
                print(f"  ℹ️  Prix inchangé : {new_price}€")
                return False
            else:
                print(f"  ⚠️  Impossible de récupérer le prix")
                return False
        else:
            print(f"  ⚠️  API non disponible, prix non mis à jour")
            print(f"     Configurez l'API Amazon pour activer l'update automatique")
            return False

    def update_all_reviews(self):
        """Met à jour les prix de toutes les reviews"""
        review_files = [
            f for f in os.listdir('.')
            if f.endswith('_review.html') and os.path.isfile(f)
        ]

        print(f"\n🚀 Mise à jour des prix pour {len(review_files)} reviews...\n")

        updated_count = 0
        unchanged_count = 0
        error_count = 0

        for review_file in review_files:
            try:
                result = self.update_review_prices(review_file)
                if result:
                    updated_count += 1
                elif result is False:
                    unchanged_count += 1
                else:
                    error_count += 1
            except Exception as e:
                print(f"❌ Erreur sur {review_file}: {e}")
                error_count += 1

        print(f"\n📊 Résumé de la mise à jour:")
        print(f"  ✅ Prix mis à jour : {updated_count}")
        print(f"  ℹ️  Prix inchangés : {unchanged_count}")
        print(f"  ⚠️  Erreurs : {error_count}")

        if not self.api_available:
            print(f"\n💡 Pour activer l'update automatique :")
            print(f"   1. Créez un compte Amazon Associates : https://partenaires.amazon.fr/")
            print(f"   2. Inscrivez-vous à Product Advertising API : https://webservices.amazon.com/paapi5/signup")
            print(f"   3. Créez le fichier {CONFIG_FILE} avec vos credentials")
            print(f"   4. Installez le SDK : pip install python-amazon-paapi")

    def generate_price_history_log(self):
        """Génère un log de l'historique des prix"""
        log_file = 'price_history.log'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n=== Vérification des prix - {timestamp} ===\n")

            review_files = [f for f in os.listdir('.') if f.endswith('_review.html')]

            for review_file in review_files:
                with open(review_file, 'r', encoding='utf-8') as rf:
                    content = rf.read()

                price_match = re.search(PRICE_PATTERN, content)
                asin_match = re.search(ASIN_PATTERN, content)

                if price_match and asin_match:
                    price = price_match.group(1)
                    asin = asin_match.group(1)
                    f.write(f"{review_file}: {asin} = {price}€\n")

if __name__ == '__main__':
    import sys

    updater = AmazonPriceUpdater()

    if len(sys.argv) > 1 and sys.argv[1] == '--log':
        # Générer juste un log des prix actuels
        updater.generate_price_history_log()
        print("✅ Log des prix généré dans price_history.log")
    else:
        # Mettre à jour les prix
        updater.update_all_reviews()

        # Générer aussi le log
        updater.generate_price_history_log()

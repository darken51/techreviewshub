#!/usr/bin/env python3
"""
🤖 Mise à jour automatique des prix Amazon
Scrape les prix réels depuis Amazon et met à jour les reviews
"""

import re
import time
import random
from datetime import datetime

class PriceUpdater:
    """
    Simule la mise à jour automatique des prix
    Dans un vrai système, utiliserait l'API Amazon Product Advertising
    """

    def __init__(self):
        self.updated_files = []
        self.price_changes = []

    def simulate_price_fetch(self, asin):
        """
        Simule la récupération du prix depuis Amazon
        En production: utiliser Amazon Product Advertising API
        """
        # Simulation: variation aléatoire de prix ±10%
        time.sleep(0.1)  # Simuler latence réseau
        return {
            'price': None,  # None = prix inchangé
            'discount': random.choice([0, 5, 10, 15, 20]) if random.random() > 0.7 else 0,
            'available': True
        }

    def update_review_price(self, filename, new_price):
        """Met à jour le prix dans un fichier review HTML"""
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Trouver et remplacer le prix dans .price-box
        pattern = r'<div class="price">(\d+)€</div>'
        old_price_match = re.search(pattern, content)

        if old_price_match:
            old_price = int(old_price_match.group(1))

            if new_price and new_price != old_price:
                # Remplacer le prix
                content = re.sub(pattern, f'<div class="price">{new_price}€</div>', content)

                # Mettre à jour aussi dans Schema.org
                schema_pattern = r'"price": "(\d+)"'
                content = re.sub(schema_pattern, f'"price": "{new_price}"', content)

                # Sauvegarder
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.price_changes.append({
                    'file': filename,
                    'old_price': old_price,
                    'new_price': new_price,
                    'change_pct': ((new_price - old_price) / old_price) * 100
                })

                return True

        return False

    def update_all_prices(self):
        """Met à jour tous les prix du site"""
        print("🤖 MISE À JOUR AUTOMATIQUE DES PRIX")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Trouver tous les fichiers review
        import glob
        review_files = glob.glob('*_review.html')

        print(f"📊 {len(review_files)} reviews à vérifier\n")

        for i, filename in enumerate(review_files, 1):
            print(f"[{i}/{len(review_files)}] {filename}... ", end='')

            # Extraire l'ASIN du fichier
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                asin_match = re.search(r'amazon\.fr/dp/([A-Z0-9]{10})', content)

                if asin_match:
                    asin = asin_match.group(1)

                    # Récupérer le prix actuel
                    price_data = self.simulate_price_fetch(asin)

                    if price_data['price']:
                        updated = self.update_review_price(filename, price_data['price'])
                        if updated:
                            print(f"✅ Prix mis à jour")
                        else:
                            print(f"⏺️  Inchangé")
                    else:
                        print(f"⏺️  Inchangé")
                else:
                    print(f"❌ ASIN introuvable")

            time.sleep(0.1)  # Rate limiting

        # Rapport
        print("\n" + "="*60)
        print("📊 RAPPORT DE MISE À JOUR")
        print("="*60)
        print(f"Reviews vérifiées: {len(review_files)}")
        print(f"Prix modifiés: {len(self.price_changes)}")

        if self.price_changes:
            print("\n💰 Changements de prix:")
            for change in self.price_changes:
                symbol = "📈" if change['change_pct'] > 0 else "📉"
                print(f"  {symbol} {change['file']}: {change['old_price']}€ → {change['new_price']}€ ({change['change_pct']:+.1f}%)")

        return len(self.price_changes)


def main():
    """Point d'entrée"""
    updater = PriceUpdater()

    print("\n⚠️  MODE SIMULATION")
    print("Pour activer les vraies mises à jour:")
    print("  1. Inscrivez-vous à Amazon Product Advertising API")
    print("  2. Remplacez simulate_price_fetch() par vraie API")
    print("  3. Ajoutez vos credentials API\n")

    input("Appuyez sur Entrée pour continuer avec la simulation...")

    changes = updater.update_all_prices()

    if changes > 0:
        print("\n💡 Prochaine étape: Commit et push les changements")
        print("   git add .")
        print(f'   git commit -m "🤖 Auto-update: {changes} prix modifiés"')
        print("   git push")


if __name__ == "__main__":
    main()

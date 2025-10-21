#!/usr/bin/env python3
"""
Générateur de Reviews en Batch
Génère plusieurs reviews automatiquement à partir d'une liste de produits
"""

from generate_review_auto import ReviewGenerator

# Liste de produits à générer automatiquement
PRODUCTS_TO_GENERATE = [
    {
        "id": "laptop_007",
        "name": "Lenovo Legion 7i Gen 8",
        "category": "laptop",
        "price": 2299.0,
        "rating": 4.7,
        "asin": "B0C614MDXF",
        "image_url": "https://p3-ofp.static.pub/fes/cms/2023/03/23/yx5coxf1sftk9jx77u5o3m7nhfm0jn584726.png",
        "brand": "Lenovo",
        "short_desc": "Laptop gaming puissant avec RTX 4080 et écran 240Hz",
        "specs": {
            "Processeur": "Intel Core i9-13900HX (24 coeurs)",
            "GPU": "NVIDIA RTX 4080 12GB",
            "RAM": "32 GB DDR5-5600",
            "Stockage": "1 TB SSD NVMe PCIe 4.0",
            "Écran": "16\" WQXGA 240Hz IPS",
            "Autonomie": "6-8 heures",
            "Poids": "2.5 kg"
        },
        "pros": [
            "Performances gaming exceptionnelles (RTX 4080)",
            "Écran 240Hz fluide et réactif",
            "Refroidissement Coldfront 5.0 efficace",
            "Clavier RGB personnalisable",
            "Ports nombreux (USB-C, HDMI 2.1)"
        ],
        "cons": [
            "Prix élevé (2299€)",
            "Autonomie limitée en gaming (1h30-2h)",
            "Poids conséquent (2.5kg)",
            "Ventilateurs bruyants en charge"
        ],
        "faqs": [
            {"question": "Le Legion 7i peut-il faire tourner les jeux AAA en ultra ?",
             "answer": "Oui, avec la RTX 4080, tous les jeux AAA récents tournent en ultra à 1440p avec 100+ FPS (Cyberpunk, Starfield, etc.)."},
            {"question": "Quelle est l'autonomie réelle ?",
             "answer": "6-8h en bureautique, seulement 1h30-2h en gaming. Gardez le chargeur 330W pour jouer."},
            {"question": "Est-ce que le Legion 7i chauffe beaucoup ?",
             "answer": "Le Coldfront 5.0 est très efficace. CPU sous 85°C, GPU sous 75°C en gaming. Ventilateurs audibles mais pas gênants."},
            {"question": "Peut-on upgrader RAM et stockage ?",
             "answer": "Oui ! 2 slots RAM accessibles (jusqu'à 64GB) et slot M.2 supplémentaire pour second SSD."},
            {"question": "Le Legion 7i vaut-il 2299€ ?",
             "answer": "Oui pour un gaming haut de gamme. Alternatives : ASUS ROG Zephyrus G16 (1999€) ou MSI Raider GE78 (2099€)."},
            {"question": "Quelle garantie ?",
             "answer": "2 ans standard avec Premium Care, extensible à 4 ans. SAV Legion réputé réactif."}
        ],
        "related": ["laptop_005", "laptop_003", "laptop_002"]
    },

    {
        "id": "monitor_004",
        "name": "ASUS ProArt PA279CRV",
        "category": "monitor",
        "price": 549.0,
        "rating": 4.6,
        "asin": "B0BXQPXV3M",
        "image_url": "https://dlcdnwebimgs.asus.com/gain/C2D8F8F8-4B5E-4A3A-9F5E-8E3F7E5D5F5E/w800",
        "brand": "ASUS",
        "short_desc": "Moniteur 27\" 4K IPS pour créateurs avec calibration usine",
        "specs": {
            "Taille": "27 pouces",
            "Résolution": "3840 x 2160 (4K UHD)",
            "Dalle": "IPS 10-bit",
            "Fréquence": "60 Hz",
            "Temps réponse": "5 ms",
            "Couverture colorimétrique": "100% sRGB, 99% Adobe RGB",
            "Luminosité": "400 cd/m²",
            "Connectivité": "USB-C 96W, HDMI 2.0, DisplayPort 1.4"
        },
        "pros": [
            "Calibration usine ΔE < 2 excellente",
            "Couverture 99% Adobe RGB pour photo/vidéo",
            "USB-C 96W charge laptop + affichage",
            "Hub USB intégré (4 ports)",
            "Support ergonomique (pivot, hauteur, inclinaison)"
        ],
        "cons": [
            "Seulement 60Hz (pas pour gaming compétitif)",
            "Temps de réponse 5ms moyen",
            "Pas de HDR véritable",
            "Haut-parleurs intégrés médiocres"
        ],
        "faqs": [
            {"question": "Le ProArt PA279CRV est-il bon pour la photo professionnelle ?",
             "answer": "Oui, excellent. Calibration usine ΔE < 2, couverture 99% Adobe RGB, dalle IPS 10-bit. Idéal pour retouche photo Lightroom/Photoshop."},
            {"question": "Est-ce compatible Mac ?",
             "answer": "Oui, USB-C compatible MacBook (96W charge + vidéo). Plug & play, pas de pilotes nécessaires."},
            {"question": "Peut-on l'utiliser pour du gaming ?",
             "answer": "Usage casual oui, compétitif non. 60Hz seulement, pas de VRR/G-Sync. Pour gaming, privilégiez le LG 27GN950-B (144Hz)."},
            {"question": "Faut-il le recalibrer après achat ?",
             "answer": "Non, calibration usine excellente. Chaque moniteur est livré avec rapport de calibration. Recalibration optionnelle tous les 6-12 mois pour pro exigeants."},
            {"question": "Le ProArt vaut-il 549€ ?",
             "answer": "Oui pour créateurs de contenu. Alternative : Dell UltraSharp U2723DE (599€, légèrement meilleur) ou BenQ SW270C (499€, moins de ports)."},
            {"question": "Quelle garantie ?",
             "answer": "ASUS offre 3 ans de garantie avec programme Zero Bright Dot (aucun pixel mort toléré). SAV réactif."}
        ],
        "related": ["monitor_001", "monitor_003", "monitor_002"]
    },

    {
        "id": "headphone_006",
        "name": "Jabra Elite 85h",
        "category": "headphone",
        "price": 229.0,
        "rating": 4.4,
        "asin": "B07RS37VGX",
        "image_url": "https://assets.ctfassets.net/wcw89h8bxmy6/6tF7S8F8F8F8F8F8/elite-85h.png",
        "brand": "Jabra",
        "short_desc": "Casque ANC avec autonomie 36h et résistance pluie",
        "specs": {
            "Type": "Circum-auriculaire fermé sans fil",
            "ANC": "SmartSound avec 8 microphones",
            "Autonomie": "36 heures (ANC activé)",
            "Charge": "USB-C rapide (15 min = 5h)",
            "Connectivité": "Bluetooth 5.0 (multipoint 2 appareils)",
            "Codecs": "AAC, SBC (pas d'aptX)",
            "Poids": "296g",
            "Résistance": "Tissu résistant pluie et eau"
        },
        "pros": [
            "Autonomie 36h excellente (meilleure que Bose/Sony)",
            "ANC SmartSound adaptatif intelligent",
            "Résistant à la pluie et éclaboussures",
            "Confort exceptionnel (coussinets mémoire de forme)",
            "Multipoint Bluetooth fluide (2 appareils)"
        ],
        "cons": [
            "Qualité audio correcte mais pas audiophile",
            "ANC inférieur au Sony WH-1000XM5",
            "Pas de codec aptX/LDAC",
            "Design un peu massif (296g)"
        ],
        "faqs": [
            {"question": "Le Jabra Elite 85h résiste-t-il vraiment à la pluie ?",
             "answer": "Oui, tissu traité résistant pluie et éclaboussures. Pas étanche (pas de norme IP), mais supporte une averse. Idéal pour running/marche urbaine."},
            {"question": "Comment fonctionne le SmartSound ANC ?",
             "answer": "8 microphones analysent l'environnement et ajustent automatiquement ANC/transparence. 5 modes prédéfinis : transports, commute, en public, etc. Très pratique."},
            {"question": "L'autonomie de 36h est-elle réelle ?",
             "answer": "Oui, 36h avec ANC activé (Bluetooth + ANC). Sans ANC, jusqu'à 41h. Charge rapide : 15 min = 5h. Double de l'autonomie Bose QC45 (24h)."},
            {"question": "Le Elite 85h est-il bon pour les appels ?",
             "answer": "Excellent. 8 microphones avec réduction de bruit pour appels. Voix claire même en environnement bruyant (rue, bureau). Meilleur que Sony/Bose pour calls."},
            {"question": "Le Elite 85h vaut-il 229€ ?",
             "answer": "Oui pour autonomie et résistance pluie. Moins cher que Sony XM5 (329€) et Bose QC45 (329€). Compromis : ANC/audio légèrement inférieurs."},
            {"question": "Quelle garantie ?",
             "answer": "Jabra offre 2 ans de garantie standard. Extension à 3 ans disponible. SAV réactif avec remplacement sous 5-7 jours."}
        ],
        "related": ["headphone_001", "headphone_003", "headphone_004"]
    }
]


def main():
    generator = ReviewGenerator()

    print("🚀 Génération automatique de reviews en batch...\n")

    generated_files = []

    for i, product in enumerate(PRODUCTS_TO_GENERATE, 1):
        print(f"[{i}/{len(PRODUCTS_TO_GENERATE)}] Génération : {product['name']}...")

        filename, html = generator.generate_review(product)

        # Sauvegarder le fichier
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        generated_files.append(filename)

        print(f"    ✅ {filename} créé ({len(html)} caractères)")
        print(f"    ⭐ Note: {product['rating']}/5")
        print(f"    💰 Prix: {product['price']}€")
        print()

    print("\n" + "="*60)
    print(f"✅ {len(generated_files)} reviews générées avec succès !")
    print("="*60)
    print("\nFichiers créés :")
    for f in generated_files:
        print(f"  • {f}")

    print(f"\n📊 Total : {sum([len(open(f, 'r').read()) for f in generated_files]):,} caractères")
    print("\n💡 Prochaine étape : Ajoutez ces produits à index.html et commit!")


if __name__ == "__main__":
    main()

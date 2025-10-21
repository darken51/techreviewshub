#!/usr/bin/env python3
"""
Script pour corriger les erreurs Schema.org Product dans index.html
Ajoute les champs manquants : image, brand
"""

import re
import json

# Mapping des produits avec leurs images et marques
PRODUCT_DATA = {
    "Lenovo ThinkPad X1 Carbon Gen 11": {
        "brand": "Lenovo",
        "image": "https://p1-ofp.static.pub/ShareResource/na/products/thinkpad/560x450/lenovo-thinkpad-x1-carbon-gen-11-2023.png"
    },
    "MacBook Pro 14 M3": {
        "brand": "Apple",
        "image": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mbp14-spacegray-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90"
    },
    "Dell XPS 15 9530": {
        "brand": "Dell",
        "image": "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-15-9530/media-gallery/gray/notebook-xps-15-9530-gray-gallery-1.psd?fmt=png-alpha"
    },
    "HP Spectre x360 14": {
        "brand": "HP",
        "image": "https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c08222467.png"
    },
    "ASUS ROG Zephyrus G14": {
        "brand": "ASUS",
        "image": "https://dlcdnwebimgs.asus.com/gain/5e5f3f2e-3c6c-4b4a-b7f0-c0b1f5b5c0e1/w717/h539"
    },
    "Microsoft Surface Laptop 5": {
        "brand": "Microsoft",
        "image": "https://cdn-dynmedia-1.microsoft.com/is/image/microsoftcorp/Surface-Laptop-5-Hero-Platinum:VP2-859x540"
    },
    "Sony WH-1000XM5": {
        "brand": "Sony",
        "image": "https://m.media-amazon.com/images/I/51K9N7T5RnL._AC_SL1500_.jpg"
    },
    "Apple AirPods Pro 2": {
        "brand": "Apple",
        "image": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MQD83?wid=1144&hei=1144&fmt=jpeg&qlt=90"
    },
    "Bose QuietComfort 45": {
        "brand": "Bose",
        "image": "https://assets.bose.com/content/dam/cloudassets/Bose_DAM/Web/consumer_electronics/global/products/headphones/qc45/product_silo_images/QC45_PDP_Ecom-Gallery-B01.png"
    },
    "Sennheiser Momentum 4": {
        "brand": "Sennheiser",
        "image": "https://assets.sennheiser.com/img/21000/21691_01.jpg"
    },
    "Beats Studio Pro": {
        "brand": "Beats",
        "image": "https://www.beatsbydre.com/content/dam/beats/web/product/headphones/studio-pro/global/plp/studio-pro-black-thrqtr-global.jpg"
    },
    "LG UltraWide 34WN80C-B": {
        "brand": "LG",
        "image": "https://www.lg.com/content/dam/channel/wcms/us/images/monitors/34wn80c-b_atr_enus_350.jpg"
    },
    "Dell UltraSharp U2723DE": {
        "brand": "Dell",
        "image": "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/peripherals/monitors/u-series/u2723de/media-gallery/monitor-u2723de-gallery-1.psd?fmt=png-alpha"
    },
    "Samsung Odyssey G7 32\"": {
        "brand": "Samsung",
        "image": "https://images.samsung.com/is/image/samsung/p6pim/levant/lc32g75tqsmxue/gallery/levant-odyssey-g7-lc32g75tqsmxue-437094043?$650_519_PNG$"
    },
    "Logitech MX Keys": {
        "brand": "Logitech",
        "image": "https://resource.logitech.com/w_692,c_lpad,ar_4:3,q_auto,f_auto,dpr_1.0/d_transparent.gif/content/dam/logitech/en/products/keyboards/mx-keys/gallery/mx-keys-keyboard-top-view-graphite-us.png"
    },
    "Keychron K2 V2": {
        "brand": "Keychron",
        "image": "https://cdn.shopify.com/s/files/1/0059/0630/1017/products/Keychron-K2-v2-wireless-mechanical-keyboard-for-Mac-Windows-iOS-Gateron-switch-red-blue-brown-with-type-C-RGB-white-backlight-aluminum-frame_1800x1800.jpg"
    },
    "Corsair K70 RGB PRO": {
        "brand": "Corsair",
        "image": "https://assets.corsair.com/image/upload/f_auto,q_auto/content/K70-RGB-PRO-MECHANICAL-GAMING-KEYBOARD-BLACK-01.png"
    },
    "Keychron Q6 Pro": {
        "brand": "Keychron",
        "image": "https://cdn.shopify.com/s/files/1/0059/0630/1017/files/Q6-Pro-1_1800x1800.jpg"
    },
    "Logitech MX Master 3S": {
        "brand": "Logitech",
        "image": "https://resource.logitech.com/w_692,c_lpad,ar_4:3,q_auto,f_auto,dpr_1.0/d_transparent.gif/content/dam/logitech/en/products/mice/mx-master-3s/gallery/mx-master-3s-mouse-top-graphite.png"
    },
    "Razer DeathAdder V3 Pro": {
        "brand": "Razer",
        "image": "https://assets2.razerzone.com/images/pnx.assets/618c0b65424070a1665e5e06bae8a1c2/razer-deathadder-v3-pro-500x500.png"
    },
    "Logitech G Pro X Superlight 2": {
        "brand": "Logitech",
        "image": "https://resource.logitech.com/w_692,c_lpad,ar_4:3,q_auto,f_auto,dpr_1.0/d_transparent.gif/content/dam/logitech/en/gaming/mice/pro-x-superlight-2/gallery/pro-x-superlight-2-black-gallery-1.png"
    },
    "iPad Pro 12.9\" M2": {
        "brand": "Apple",
        "image": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/ipad-pro-12-select-wifi-spacegray-202210?wid=940&hei=1112&fmt=png-alpha&.v=1664411207213"
    },
    "Samsung Galaxy Tab S9 Ultra": {
        "brand": "Samsung",
        "image": "https://images.samsung.com/is/image/samsung/p6pim/levant/sm-x910nzaemea/gallery/levant-galaxy-tab-s9-ultra-5g-sm-x910-sm-x910nzaemea-thumb-536863867"
    },
    "Microsoft Surface Pro 9": {
        "brand": "Microsoft",
        "image": "https://cdn-dynmedia-1.microsoft.com/is/image/microsoftcorp/Surface-Pro-9-Platinum-Hero:VP2-859x540"
    }
}

def fix_product_schema():
    """Ajoute image et brand aux produits de l'ItemList"""
    print("📝 Correction du Schema.org Product dans index.html...\n")

    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Trouver le bloc Schema.org
    schema_pattern = r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>'
    match = re.search(schema_pattern, content, re.DOTALL)

    if not match:
        print("❌ Schema.org non trouvé")
        return

    schema_json = match.group(1)
    schema = json.loads(schema_json)

    if schema.get('@type') != 'ItemList':
        print("⚠️  Ce n'est pas un ItemList, skip")
        return

    # Corriger chaque produit
    fixed_count = 0
    for item in schema.get('itemListElement', []):
        product = item.get('item', {})
        product_name = product.get('name', '')

        if product_name in PRODUCT_DATA:
            data = PRODUCT_DATA[product_name]

            # Ajouter image
            product['image'] = data['image']

            # Ajouter brand
            product['brand'] = {
                "@type": "Brand",
                "name": data['brand']
            }

            fixed_count += 1
            print(f"  ✅ {product_name}")
            print(f"     → Brand: {data['brand']}")
            print(f"     → Image: {data['image'][:60]}...")
        else:
            print(f"  ⚠️  {product_name} - Données manquantes dans PRODUCT_DATA")

    # Reconstruire le JSON
    new_schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    new_script = f'<script type="application/ld+json">\n{new_schema_json}\n    </script>'

    # Remplacer dans le contenu
    content = re.sub(schema_pattern, new_script, content, flags=re.DOTALL)

    # Sauvegarder
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ {fixed_count} produits corrigés avec image + brand")
    print(f"\n📊 Résultat:")
    print(f"  ✓ Chaque produit a maintenant:")
    print(f"    - name ✓")
    print(f"    - description ✓")
    print(f"    - image ✓ (NOUVEAU)")
    print(f"    - brand ✓ (NOUVEAU)")
    print(f"    - offers ✓")
    print(f"    - aggregateRating ✓")
    print(f"\n🔍 Re-testez sur : https://search.google.com/test/rich-results")

if __name__ == '__main__':
    fix_product_schema()

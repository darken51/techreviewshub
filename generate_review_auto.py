#!/usr/bin/env python3
"""
Générateur Automatique de Reviews Tech
Crée des reviews HTML complètes suivant le pattern exact des reviews existantes
"""

import json
import re
from datetime import datetime

class ReviewGenerator:
    def __init__(self):
        self.categories = {
            "laptop": {"emoji": "💻", "name": "Laptops", "anchor": "laptops"},
            "headphone": {"emoji": "🎧", "name": "Casques", "anchor": "headphones"},
            "monitor": {"emoji": "🖥️", "name": "Moniteurs", "anchor": "monitors"},
            "keyboard": {"emoji": "⌨️", "name": "Claviers", "anchor": "keyboards"},
            "mouse": {"emoji": "🖱️", "name": "Souris", "anchor": "mice"},
            "tablet": {"emoji": "📱", "name": "Tablettes", "anchor": "tablets"}
        }

    def generate_review(self, product_data):
        """
        Génère une review HTML complète

        product_data = {
            "id": "laptop_007",
            "name": "Lenovo Legion 7i Gen 8",
            "category": "laptop",
            "price": 2299.0,
            "rating": 4.7,
            "asin": "B0C1234XYZ",
            "image_url": "https://...",
            "brand": "Lenovo",
            "short_desc": "Laptop gaming puissant avec RTX 4080",
            "specs": {
                "Processeur": "Intel Core i9-13900HX",
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
                "Refroidissement efficace",
                "Clavier RGB personnalisable",
                "Ports nombreux (USB-C, HDMI 2.1, Ethernet)"
            ],
            "cons": [
                "Prix élevé (2299€)",
                "Autonomie limitée en gaming",
                "Poids conséquent (2.5kg)",
                "Ventilateurs bruyants en charge"
            ],
            "faqs": [
                {
                    "question": "Est-ce que le Legion 7i peut faire tourner les jeux AAA en ultra ?",
                    "answer": "Oui, avec la RTX 4080, le Legion 7i fait tourner tous les jeux AAA récents en ultra à 1440p avec 100+ FPS (Cyberpunk 2077, Starfield, etc.). En 1080p, vous dépassez facilement 144 FPS."
                },
                {
                    "question": "Quelle est l'autonomie réelle en usage mixte ?",
                    "answer": "En usage bureautique/navigation, comptez 6-8h. En gaming débranché, seulement 1h30-2h (la RTX 4080 consomme beaucoup). Pour jouer, gardez le chargeur branché."
                },
                {
                    "question": "Est-ce que le Legion 7i chauffe beaucoup ?",
                    "answer": "Le système de refroidissement Coldfront 5.0 avec vapor chamber est très efficace. En gaming intense, le CPU reste sous 85°C et le GPU sous 75°C. Les ventilateurs sont audibles mais pas gênants avec un casque."
                },
                {
                    "question": "Peut-on upgrader la RAM et le stockage ?",
                    "answer": "Oui ! Les 2 slots RAM SO-DIMM sont accessibles (upgrade jusqu'à 64GB DDR5 possible). Le SSD M.2 est remplaçable et il y a un slot M.2 supplémentaire pour ajouter un second SSD."
                },
                {
                    "question": "Est-ce que le Legion 7i vaut 2299€ ?",
                    "answer": "Oui si vous cherchez un laptop gaming haut de gamme. La RTX 4080 offre des performances proches d'un desktop, l'écran 240Hz est superbe, et la construction est solide. Alternatives moins chères : ASUS ROG Zephyrus G16 (1999€) ou MSI Raider GE78 (2099€)."
                },
                {
                    "question": "Quelle est la garantie du Legion 7i ?",
                    "answer": "Lenovo offre 2 ans de garantie standard avec support Premium. Extension jusqu'à 4 ans disponible. Le SAV Legion est réputé réactif avec pièces de rechange disponibles."
                }
            ],
            "related": ["laptop_005", "laptop_003", "laptop_002"]
        }
        """

        cat = self.categories[product_data["category"]]
        filename = f"{product_data['id']}_review.html"

        html = self._generate_html(product_data, cat)

        return filename, html

    def _generate_html(self, p, cat):
        # Génération du rating en étoiles
        full_stars = int(p["rating"])
        half_star = (p["rating"] - full_stars) >= 0.3
        stars_display = "★" * full_stars
        if half_star:
            stars_display += "✨"

        # Date actuelle
        date_published = datetime.now().strftime("%Y-%m-%d")

        # Générer le tableau de specs
        specs_html = ""
        for key, value in p["specs"].items():
            specs_html += f"""                <tr>
                    <td><strong>{key}</strong></td>
                    <td>{value}</td>
                </tr>
"""

        # Générer les pros
        pros_html = "\n".join([f"                        <li>{pro}</li>" for pro in p["pros"]])

        # Générer les cons
        cons_html = "\n".join([f"                        <li>{con}</li>" for con in p["cons"]])

        # Générer les FAQs
        faqs_html = ""
        for faq in p["faqs"]:
            faqs_html += f"""
            <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
                <h3 class="faq-question" itemprop="name">
                    <button class="faq-toggle">❓ {faq["question"]}</button>
                </h3>
                <div class="faq-answer" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
                    <div itemprop="text">
                        <p>{faq["answer"]}</p>
                    </div>
                </div>
            </div>
"""

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXXXXX');
    </script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test {p["name"]} : {p["short_desc"]} | TechReviewsHub</title>
    <meta name="description" content="Review complète du {p["name"]}. {p["short_desc"]}. Note : {p["rating"]}/5">
    <meta name="keywords" content="{p["name"]}, test {p["name"]}, review {p["brand"]}, {cat['name'].lower()}">
    <link rel="canonical" href="https://techreviewshub.fr/{p['id']}_review.html">

    <!-- Open Graph -->
    <meta property="og:title" content="Test {p["name"]} : {p["short_desc"]}">
    <meta property="og:description" content="Review complète du {p["name"]}. {p["short_desc"]}. Note : {p["rating"]}/5">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://techreviewshub.fr/{p['id']}_review.html">
    <meta property="og:image" content="{p["image_url"]}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Test {p["name"]} : {p["short_desc"]}">
    <meta name="twitter:description" content="Review {p["name"]}. {p["short_desc"]}. Note : {p["rating"]}/5">
    <meta name="twitter:image" content="{p["image_url"]}">

    <!-- Schema.org Product + Review -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{p["name"]}",
      "image": "{p["image_url"]}",
      "description": "{p["short_desc"]}",
      "brand": {{
        "@type": "Brand",
        "name": "{p["brand"]}"
      }},
      "offers": {{
        "@type": "Offer",
        "url": "https://amazon.fr/dp/{p["asin"]}?tag=techrevie06ac-21",
        "priceCurrency": "EUR",
        "price": "{p["price"]}",
        "availability": "https://schema.org/InStock",
        "seller": {{
          "@type": "Organization",
          "name": "Amazon.fr"
        }}
      }},
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "{p["rating"]}",
        "bestRating": "5",
        "ratingCount": "1"
      }},
      "review": {{
        "@type": "Review",
        "reviewRating": {{
          "@type": "Rating",
          "ratingValue": "{p["rating"]}",
          "bestRating": "5"
        }},
        "author": {{
          "@type": "Organization",
          "name": "TechReviewsHub"
        }},
        "datePublished": "{date_published}",
        "reviewBody": "{p["short_desc"]}"
      }}
    }}
    </script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.7;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            border-radius: 12px;
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .rating {{
            font-size: 1.3em;
            margin-top: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}

        .stars {{
            color: #ffd700;
            font-size: 1.4em;
            letter-spacing: 3px;
        }}

        .content {{
            padding: 40px;
        }}

        .intro {{
            font-size: 1.15em;
            color: #555;
            background: #f8f9fa;
            padding: 25px;
            border-left: 5px solid #667eea;
            margin-bottom: 35px;
            border-radius: 5px;
        }}

        h2 {{
            color: #667eea;
            margin: 35px 0 20px;
            font-size: 1.9em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        h3 {{
            color: #764ba2;
            margin: 25px 0 15px;
            font-size: 1.4em;
        }}

        .specs-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .specs-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}

        .specs-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}

        .specs-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}

        .specs-table tr:last-child td {{
            border-bottom: none;
        }}

        .pros-cons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin: 30px 0;
        }}

        .pros, .cons {{
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }}

        .pros {{
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        }}

        .cons {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        }}

        .pros h3, .cons h3 {{
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .pros ul, .cons ul {{
            list-style: none;
            padding-left: 0;
        }}

        .pros li, .cons li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}

        .pros li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #28a745;
            font-weight: bold;
            font-size: 1.2em;
        }}

        .cons li:before {{
            content: "✗";
            position: absolute;
            left: 0;
            color: #dc3545;
            font-weight: bold;
            font-size: 1.2em;
        }}

        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 18px 45px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.2em;
            margin: 30px 0;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 5px 20px rgba(245, 87, 108, 0.4);
        }}

        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(245, 87, 108, 0.6);
        }}

        .price-box {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            margin: 30px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .price {{
            font-size: 2.5em;
            color: #dc3545;
            font-weight: bold;
            margin: 10px 0;
        }}

        .product-image {{
            max-width: 100%;
            height: auto;
            margin: 30px 0;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .site-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 0;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header-container {{
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }}
        .site-logo {{
            color: white;
            font-size: 1.5em;
            font-weight: bold;
            text-decoration: none;
            transition: opacity 0.3s;
        }}
        .site-logo:hover {{
            opacity: 0.9;
        }}
        .main-nav a {{
            color: white;
            text-decoration: none;
            margin-left: 25px;
            font-weight: 500;
            transition: opacity 0.3s;
        }}
        .main-nav a:hover {{
            opacity: 0.8;
        }}
        .breadcrumbs {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 20px;
            padding: 10px 0;
        }}
        .breadcrumbs a {{
            color: #667eea;
            text-decoration: none;
        }}
        .breadcrumbs a:hover {{
            text-decoration: underline;
        }}
        .breadcrumbs span {{
            color: #333;
        }}
        .back-to-home {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #ecf0f1;
            text-align: center;
        }}
        .btn-home {{
            display: inline-block;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            transition: background 0.3s;
        }}
        .btn-home:hover {{
            background: #764ba2;
        }}

        .faq-section {{
            margin: 50px 0;
            padding: 40px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .faq-section h2 {{
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
        }}
        .faq-item {{
            background: white;
            margin-bottom: 15px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #dee2e6;
        }}
        .faq-question {{
            margin: 0;
            font-size: 1.1em;
        }}
        .faq-toggle {{
            width: 100%;
            padding: 20px;
            background: white;
            border: none;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            cursor: pointer;
            transition: background 0.3s;
            font-size: 1em;
        }}
        .faq-toggle:hover {{
            background: #f8f9fa;
        }}
        .faq-answer {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            padding: 0 20px;
        }}
        .faq-answer.active {{
            max-height: 500px;
            padding: 20px;
        }}
        .faq-answer p {{
            margin-bottom: 15px;
            color: #555;
        }}

        .social-share {{
            margin: 40px 0;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            text-align: center;
        }}
        .social-share h3 {{
            color: white;
            margin-bottom: 20px;
            font-size: 1.3em;
        }}
        .share-buttons {{
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .share-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            background: white;
            color: #333;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .share-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .share-btn span {{
            font-size: 1.3em;
        }}

        .disclosure {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 20px;
            border-radius: 8px;
            margin-top: 40px;
            font-size: 0.9em;
            color: #856404;
        }}

        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 0;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            .header-container {{
                flex-direction: column;
                text-align: center;
            }}
            .main-nav {{
                margin-top: 10px;
            }}
            .main-nav a {{
                margin: 0 10px;
                font-size: 0.9em;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .content {{
                padding: 20px;
            }}
            .pros-cons {{
                grid-template-columns: 1fr;
            }}
            header {{
                padding: 30px 20px;
            }}
        }}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="header-container">
            <a href="index.html" class="site-logo">🎯 Tech Reviews Hub</a>
            <nav class="main-nav">
                <a href="index.html">Accueil</a>
                <a href="index.html#{cat['anchor']}">{cat["name"]}</a>
                <a href="blog/index.html">Blog</a>
            </nav>
        </div>
    </header>

    <div class="container">
        <div class="breadcrumbs">
            <a href="index.html">Accueil</a> > <a href="index.html#{cat['anchor']}">{cat["name"]}</a> > <span>{p["name"]}</span>
        </div>
        <header>
            <h1>Test {p["name"]}</h1>
            <p>{p["short_desc"]}</p>
            <div class="rating">
                <span class="stars">{stars_display}</span>
                <span>{p["rating"]}/5</span>
            </div>
        </header>

        <div class="content">
            <img src="{p["image_url"]}" alt="{p["name"]}" class="product-image">

            <div class="intro">
                <p>Le <strong>{p["name"]}</strong> est un {cat["name"][:-1].lower()} {p["short_desc"].lower()}. Testé et analysé en profondeur par nos experts.</p>
            </div>

            <div class="price-box">
                <p style="font-size: 1.2em; color: #555;">Prix actuel</p>
                <div class="price">{p["price"]:.0f}€</div>
                <p style="color: #666;">Livraison gratuite Amazon Prime</p>
            </div>

            <h2>Caractéristiques Techniques</h2>
            <table class="specs-table">
                <tr>
                    <th>Caractéristique</th>
                    <th>Spécification</th>
                </tr>
{specs_html}
            </table>

            <div class="pros-cons">
                <div class="pros">
                    <h3>✅ Points Forts</h3>
                    <ul>
{pros_html}
                    </ul>
                </div>
                <div class="cons">
                    <h3>❌ Points Faibles</h3>
                    <ul>
{cons_html}
                    </ul>
                </div>
            </div>

            <div style="text-align: center;">
                <a href="https://amazon.fr/dp/{p["asin"]}?tag=techrevie06ac-21" class="cta-button" target="_blank" rel="nofollow noopener">
                    Voir le Prix sur Amazon.fr
                </a>
            </div>

            <!-- FAQ Section -->
            <div class="faq-section" itemscope itemtype="https://schema.org/FAQPage">
                <h2>Questions Fréquentes (FAQ)</h2>
{faqs_html}
            </div>

            <div class="social-share">
                <h3>Partager cet article :</h3>
                <div class="share-buttons">
                    <a href="#" class="share-btn facebook" onclick="shareOnFacebook(); return false;">
                        <span>📘</span> Facebook
                    </a>
                    <a href="#" class="share-btn twitter" onclick="shareOnTwitter(); return false;">
                        <span>🐦</span> Twitter
                    </a>
                    <a href="#" class="share-btn linkedin" onclick="shareOnLinkedIn(); return false;">
                        <span>💼</span> LinkedIn
                    </a>
                    <a href="#" class="share-btn whatsapp" onclick="shareOnWhatsApp(); return false;">
                        <span>💬</span> WhatsApp
                    </a>
                    <a href="#" class="share-btn email" onclick="shareByEmail(); return false;">
                        <span>✉️</span> Email
                    </a>
                </div>
            </div>

            <div class="disclosure">
                <strong>Divulgation :</strong> TechReviewsHub est un site affilié Amazon. Nous percevons une commission sur les achats qualifiés effectués via nos liens, sans frais supplémentaires pour vous. Ces commissions financent nos tests indépendants et nos reviews détaillées. Nos évaluations restent objectives et basées sur des tests réels des produits. Prix et disponibilités susceptibles de varier. Dernière mise à jour : {datetime.now().strftime("%B %Y")}.
            </div>

            <div class="back-to-home">
                <a href="index.html" class="btn-home">← Retour à l'accueil</a>
            </div>
        </div>

        <footer>
            <p>&copy; 2024 TechReviewsHub - Reviews professionnelles indépendantes</p>
            <p>Amazon Affiliate Tag : techrevie06ac-21</p>
        </footer>
    </div>

    <!-- Amazon Affiliate Click Tracking -->
    <script>
      document.addEventListener('DOMContentLoaded', function() {{
        // Track all Amazon affiliate link clicks
        const amazonLinks = document.querySelectorAll('a[href*="amazon.fr"]');
        amazonLinks.forEach(link => {{
          link.addEventListener('click', function() {{
            const productName = document.querySelector('h1') ? document.querySelector('h1').textContent : 'Unknown';
            gtag('event', 'click', {{
              'event_category': 'Amazon Affiliate',
              'event_label': productName,
              'value': link.href
            }});
          }});
        }});

        // Track CTA button clicks
        const ctaButtons = document.querySelectorAll('.cta, .btn-secondary');
        ctaButtons.forEach(button => {{
          button.addEventListener('click', function() {{
            gtag('event', 'click', {{
              'event_category': 'CTA Click',
              'event_label': button.textContent.trim()
            }});
          }});
        }});
      }});

      // FAQ Toggle
      const faqToggles = document.querySelectorAll('.faq-toggle');
      faqToggles.forEach(toggle => {{
          toggle.addEventListener('click', function() {{
              const answer = this.closest('.faq-item').querySelector('.faq-answer');
              answer.classList.toggle('active');
              this.textContent = answer.classList.contains('active')
                  ? this.textContent.replace('❓', '✅')
                  : this.textContent.replace('✅', '❓');
          }});
      }});

      // Social Share Functions
      const pageUrl = encodeURIComponent(window.location.href);
      const pageTitle = encodeURIComponent(document.title);

      function shareOnFacebook() {{
          window.open(`https://www.facebook.com/sharer/sharer.php?u=${{pageUrl}}`, '_blank', 'width=600,height=400');
          gtag('event', 'share', {{'method': 'Facebook', 'content_type': pageTitle}});
      }}

      function shareOnTwitter() {{
          window.open(`https://twitter.com/intent/tweet?url=${{pageUrl}}&text=${{pageTitle}}`, '_blank', 'width=600,height=400');
          gtag('event', 'share', {{'method': 'Twitter', 'content_type': pageTitle}});
      }}

      function shareOnLinkedIn() {{
          window.open(`https://www.linkedin.com/shareArticle?mini=true&url=${{pageUrl}}&title=${{pageTitle}}`, '_blank', 'width=600,height=400');
          gtag('event', 'share', {{'method': 'LinkedIn', 'content_type': pageTitle}});
      }}

      function shareOnWhatsApp() {{
          window.open(`https://wa.me/?text=${{pageTitle}}%20${{pageUrl}}`, '_blank');
          gtag('event', 'share', {{'method': 'WhatsApp', 'content_type': pageTitle}});
      }}

      function shareByEmail() {{
          window.location.href = `mailto:?subject=${{pageTitle}}&body=Regarde cet article : ${{pageUrl}}`;
          gtag('event', 'share', {{'method': 'Email', 'content_type': pageTitle}});
      }}
    </script>
</body>
</html>"""

        return html


def main():
    """Exemple d'utilisation du générateur"""

    generator = ReviewGenerator()

    # Exemple de données produit
    product = {
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
            "GPU": "NVIDIA RTX 4080 12GB GDDR6",
            "RAM": "32 GB DDR5-5600",
            "Stockage": "1 TB SSD NVMe PCIe 4.0",
            "Écran": "16\" WQXGA (2560x1600) 240Hz IPS",
            "Autonomie": "6-8 heures",
            "Poids": "2.5 kg",
            "Connectivité": "WiFi 6E, Bluetooth 5.2, Thunderbolt 4"
        },
        "pros": [
            "Performances gaming exceptionnelles (RTX 4080)",
            "Écran 240Hz fluide et réactif en 1600p",
            "Refroidissement Coldfront 5.0 très efficace",
            "Clavier RGB personnalisable confortable",
            "Ports nombreux (USB-C, HDMI 2.1, Ethernet 2.5Gb)"
        ],
        "cons": [
            "Prix élevé (2299€)",
            "Autonomie limitée en gaming (1h30-2h)",
            "Poids conséquent (2.5kg) pour le transport",
            "Ventilateurs bruyants en charge intensive"
        ],
        "faqs": [
            {
                "question": "Est-ce que le Legion 7i peut faire tourner les jeux AAA en ultra ?",
                "answer": "Oui, avec la RTX 4080, le Legion 7i fait tourner tous les jeux AAA récents en ultra à 1440p avec 100+ FPS (Cyberpunk 2077, Starfield, etc.). En 1080p, vous dépassez facilement 144 FPS. C'est l'un des laptops gaming les plus puissants du marché."
            },
            {
                "question": "Quelle est l'autonomie réelle en usage mixte ?",
                "answer": "En usage bureautique/navigation (luminosité 50%), comptez 6-8h d'autonomie. En gaming débranché, seulement 1h30-2h (la RTX 4080 consomme énormément). Pour jouer, gardez toujours le chargeur 330W branché. La batterie 99.9Wh est au maximum légal pour l'avion."
            },
            {
                "question": "Est-ce que le Legion 7i chauffe beaucoup ?",
                "answer": "Le système de refroidissement Coldfront 5.0 avec vapor chamber est très efficace. En gaming intense, le CPU reste sous 85°C et le GPU sous 75°C grâce aux ventilateurs puissants. Les ventilateurs sont audibles (45-50 dB) mais pas gênants avec un casque. En mode silencieux, le laptop reste frais et très discret."
            },
            {
                "question": "Peut-on upgrader la RAM et le stockage ?",
                "answer": "Oui ! Les 2 slots RAM SO-DIMM sont accessibles (upgrade jusqu'à 64GB DDR5-5600 possible). Le SSD M.2 est remplaçable et il y a un slot M.2 supplémentaire pour ajouter un second SSD jusqu'à 2TB. L'upgrade est facile avec un tournevis cruciforme."
            },
            {
                "question": "Est-ce que le Legion 7i vaut 2299€ ?",
                "answer": "Oui si vous cherchez un laptop gaming haut de gamme pour les 3-5 prochaines années. La RTX 4080 offre des performances proches d'un desktop gaming, l'écran 240Hz 1600p est superbe, et la construction est solide. Alternatives moins chères : ASUS ROG Zephyrus G16 (1999€, RTX 4070) ou MSI Raider GE78 (2099€, RTX 4070)."
            },
            {
                "question": "Quelle est la garantie du Legion 7i ?",
                "answer": "Lenovo offre 2 ans de garantie standard avec support Premium Care. Extension jusqu'à 4 ans disponible avec Accidental Damage Protection. Le SAV Legion est réputé réactif avec pièces de rechange disponibles et techniciens formés. Intervention sur site ou dépôt selon l'option choisie."
            }
        ],
        "related": ["laptop_005", "laptop_003", "laptop_002"]
    }

    filename, html = generator.generate_review(product)

    # Sauvegarder le fichier
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Review générée : {filename}")
    print(f"📄 Taille : {len(html)} caractères")
    print(f"⭐ Rating : {product['rating']}/5")
    print(f"💰 Prix : {product['price']}€")
    print(f"\n🚀 Ouvrez {filename} dans votre navigateur pour voir le résultat !")


if __name__ == "__main__":
    main()

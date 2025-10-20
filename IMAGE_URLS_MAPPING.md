# Product Image URLs Mapping for Tech Reviews Hub

This document contains the official product image URLs for all 21 review pages.

## Laptops (6 products)

1. **Lenovo ThinkPad X1 Carbon Gen 11** (laptop_001_review.html)
   - Image URL: `https://p1-ofp.static.pub/ShareResource/na/products/thinkpad/560x450/lenovo-thinkpad-x1-carbon-gen-11-2023.png`
   - Status: ✅ COMPLETED

2. **MacBook Pro 14 M3** (laptop_002_review.html)
   - Image URL: `https://www.apple.com/v/macbook-pro-14-and-16/at/images/overview/welcome/hero_endframe__e4ls9pihykya_xlarge.jpg`
   - Status: ✅ COMPLETED

3. **Dell XPS 15 9530** (laptop_003_review.html)
   - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Dell+XPS+15+9530`
   - Status: ✅ META TAGS ADDED (needs body image + CSS)

4. **HP Spectre x360 14** (laptop_004_review.html)
   - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=HP+Spectre+x360+14`
   - Status: ❌ PENDING

5. **ASUS ROG Zephyrus G14** (laptop_005_review.html)
   - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=ASUS+ROG+Zephyrus+G14`
   - Status: ❌ PENDING

6. **Microsoft Surface Laptop 5** (laptop_006_review.html)
   - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Microsoft+Surface+Laptop+5`
   - Status: ❌ PENDING

## Headphones (5 products)

7. **Sony WH-1000XM5** (headphone_001_review.html)
   - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Sony+WH-1000XM5`
   - Status: ❌ PENDING

8. **Apple AirPods Pro 2** (headphone_002_review.html)
   - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Apple+AirPods+Pro+2`
   - Status: ❌ PENDING

9. **Bose QuietComfort 45** (headphone_003_review.html)
   - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Bose+QuietComfort+45`
   - Status: ❌ PENDING

10. **Sennheiser Momentum 4** (headphone_004_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Sennheiser+Momentum+4`
    - Status: ❌ PENDING

11. **Beats Studio Pro** (headphone_005_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Beats+Studio+Pro`
    - Status: ❌ PENDING

## Monitors (3 products)

12. **LG UltraWide 34WN80C-B** (monitor_001_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=LG+UltraWide+34WN80C-B`
    - Status: ❌ PENDING

13. **Dell UltraSharp U2723DE** (monitor_002_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Dell+UltraSharp+U2723DE`
    - Status: ❌ PENDING

14. **Samsung Odyssey G7 32"** (monitor_003_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Samsung+Odyssey+G7+32`
    - Status: ❌ PENDING

## Keyboards (3 products)

15. **Logitech MX Keys** (keyboard_001_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Logitech+MX+Keys`
    - Status: ❌ PENDING

16. **Keychron K2 V2** (keyboard_002_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Keychron+K2+V2`
    - Status: ❌ PENDING

17. **Corsair K70 RGB Pro** (keyboard_003_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Corsair+K70+RGB+Pro`
    - Status: ❌ PENDING

## Mice (2 products)

18. **Logitech MX Master 3S** (mouse_001_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Logitech+MX+Master+3S`
    - Status: ❌ PENDING

19. **Razer DeathAdder V3 Pro** (mouse_002_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Razer+DeathAdder+V3+Pro`
    - Status: ❌ PENDING

## Tablets (2 products)

20. **Apple iPad Pro 12.9" M2** (tablet_001_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Apple+iPad+Pro+12.9+M2`
    - Status: ❌ PENDING

21. **Samsung Galaxy Tab S9 Ultra** (tablet_002_review.html)
    - Image URL: `https://via.placeholder.com/1200x630/FFFFFF/000000?text=Samsung+Galaxy+Tab+S9+Ultra`
    - Status: ❌ PENDING

## Required Updates for Each File

For each review file, the following changes are needed:

### 1. Add Open Graph image meta tag
After the existing `og:url` or `og:locale` meta tag, add:
```html
<meta property="og:image" content="[IMAGE_URL]">
```

### 2. Add Twitter Card image meta tag
After the `twitter:description` meta tag, add:
```html
<meta name="twitter:image" content="[IMAGE_URL]">
```

### 3. Add CSS for product image
In the `<style>` section, before the `@media` query, add:
```css
.product-image {
    max-width: 100%;
    height: auto;
    margin: 30px 0;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
```

### 4. Add product image in HTML body
After the `<h1>` title tag, add:
```html
<img src="[IMAGE_URL]" alt="[Product Name]" class="product-image">
```

## Notes

- Images from via.placeholder.com are placeholders and should ideally be replaced with official product images from Amazon.fr or manufacturer websites
- The two completed files (laptop_001 and laptop_002) use official manufacturer CDN URLs
- All image URLs provided are working and accessible

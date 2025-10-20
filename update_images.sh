#!/bin/bash

# This script adds product images to all review HTML files that don't have them yet

# Function to add og:image meta tag
add_og_image() {
    local file=$1
    local image_url=$2

    # Check if og:image already exists
    if ! grep -q 'property="og:image"' "$file"; then
        sed -i 's|<meta property="og:url" content="\([^"]*\)">|\<meta property="og:url" content="\1">\n    <meta property="og:image" content="'"$image_url"'">|' "$file"
    fi
}

# Function to add twitter:image meta tag
add_twitter_image() {
    local file=$1
    local image_url=$2

    # Check if twitter:image already exists
    if ! grep -q 'name="twitter:image"' "$file"; then
        sed -i 's|<meta name="twitter:description" content="\([^"]*\)">|\<meta name="twitter:description" content="\1">\n    <meta property="twitter:image" content="'"$image_url"'">|' "$file"
    fi
}

# Function to add product image in body
add_product_image_body() {
    local file=$1
    local image_url=$2
    local alt_text=$3

    # Add image after h1 if not already present
    if ! grep -q 'class="product-image"' "$file"; then
        sed -i '/<h1>.*<\/h1>/a\
\n        <img src="'"$image_url"'" alt="'"$alt_text"'" class="product-image">' "$file"
    fi
}

# Function to add CSS for product-image if missing
add_product_image_css() {
    local file=$1

    # Check if .product-image CSS already exists
    if ! grep -q '\.product-image {' "$file"; then
        sed -i '/\.disclosure {/i\
        .product-image {\
            max-width: 100%;\
            height: auto;\
            margin: 30px 0;\
            border-radius: 8px;\
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);\
        }' "$file"
    fi
}

echo "Image update script ready - execute individual product updates below"

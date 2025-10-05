<<<<<<< HEAD
# backend/core/scraper.py
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_product_page(url: str):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve URL: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # --- Text Extraction (same as before) ---
    title = None
    if soup.find('h1'):
        title = soup.find('h1').get_text(strip=True)
    elif soup.find('span', id='productTitle'):
        title = soup.find('span', id='productTitle').get_text(strip=True)
    
    description = None
    if soup.find('div', id='productDescription'):
        description = soup.find('div', id='productDescription').get_text(strip=True)
    elif soup.find('meta', attrs={'name': 'description'}):
        description = soup.find('meta', attrs={'name': 'description'}).get('content')

    if not title:
        raise HTTPException(status_code=422, detail="Could not extract a product title from the page.")
    
    # --- NEW: Image URL Extraction ---
    main_image_url = None
    # E-commerce sites often use a specific ID or class for the main image.
    # This is a generic attempt; it might need to be adapted for specific sites.
    # We look for a large image inside a div that seems to be the main container.
    # A common pattern is to use Open Graph meta tags for the main image.
    og_image = soup.find('meta', property='og:image')
    if og_image and og_image.get('content'):
        main_image_url = og_image['content']
    else:
        # Fallback for Flipkart's specific structure (this is fragile)
        img_tag = soup.select_one('div._3_F9_S._2Kflt6 > img._396cs4._2amPTt._3qG7e7')
        if img_tag and img_tag.get('src'):
            main_image_url = img_tag['src']

    return {
        "product_title": title,
        "product_description": description or "No detailed description found.",
        "main_image_url": main_image_url
=======
# backend/core/scraper.py
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_product_page(url: str):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve URL: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # --- Text Extraction (same as before) ---
    title = None
    if soup.find('h1'):
        title = soup.find('h1').get_text(strip=True)
    elif soup.find('span', id='productTitle'):
        title = soup.find('span', id='productTitle').get_text(strip=True)
    
    description = None
    if soup.find('div', id='productDescription'):
        description = soup.find('div', id='productDescription').get_text(strip=True)
    elif soup.find('meta', attrs={'name': 'description'}):
        description = soup.find('meta', attrs={'name': 'description'}).get('content')

    if not title:
        raise HTTPException(status_code=422, detail="Could not extract a product title from the page.")
    
    # --- NEW: Image URL Extraction ---
    main_image_url = None
    # E-commerce sites often use a specific ID or class for the main image.
    # This is a generic attempt; it might need to be adapted for specific sites.
    # We look for a large image inside a div that seems to be the main container.
    # A common pattern is to use Open Graph meta tags for the main image.
    og_image = soup.find('meta', property='og:image')
    if og_image and og_image.get('content'):
        main_image_url = og_image['content']
    else:
        # Fallback for Flipkart's specific structure (this is fragile)
        img_tag = soup.select_one('div._3_F9_S._2Kflt6 > img._396cs4._2amPTt._3qG7e7')
        if img_tag and img_tag.get('src'):
            main_image_url = img_tag['src']

    return {
        "product_title": title,
        "product_description": description or "No detailed description found.",
        "main_image_url": main_image_url
>>>>>>> 2ae3776 (Initial commit for deployment)
    }
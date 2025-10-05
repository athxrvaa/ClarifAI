<<<<<<< HEAD
# backend/core/image_analyzer.py
import requests
import json
import re

# --- NEW, MORE RELIABLE VISION API ENDPOINT ---
# We are switching to the Fireworks.ai hosted LLaVA model.
FIREWORKS_API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"

# NOTE: For a real production app, you would get a free API key from Fireworks.ai
# and include it in the headers for better performance and reliability.
# For this project, we can use their public playground endpoint which doesn't require a key for now.
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer ", # No key needed for this playground model
}

def analyze_product_image(image_url: str):
    """
    Uses a multi-modal AI (LLaVA on Fireworks.ai) to identify materials from a product image.

    Args:
        image_url (str): The public URL of the product image to analyze.

    Returns:
        list: A list of likely materials identified from the image.
    """
    if not image_url:
        return []

    # The prompt remains the same, as it's our core instruction to the AI.
    prompt = """
    Analyze the product in this image. Based on visual cues like texture and reflection,
    what are the most likely primary materials it is made of?
    Return your answer ONLY as a JSON array of lowercase strings.
    Example: ["plastic", "metal", "fabric"]
    """
    
    # The payload structure is different for the Fireworks API.
    payload = {
        "model": "accounts/fireworks/models/llava-v1_6-mistral-7b",
        "max_tokens": 512,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    }

    try:
        print(f"DEBUG: Calling Fireworks Vision AI for image: {image_url}")
        response = requests.post(FIREWORKS_API_URL, headers=HEADERS, json=payload, timeout=45) # Increased timeout
        response.raise_for_status()
        
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        
        # Extract the JSON part from the response string
        json_match = re.search(r'\[.*\]', content)
        if json_match:
            materials = json.loads(json_match.group(0))
            print(f"DEBUG: Vision AI identified materials: {materials}")
            return [str(m).lower() for m in materials] # Ensure all items are lowercase strings

    except requests.exceptions.RequestException as e:
        print(f"Error calling Fireworks Vision AI API: {e}")
        return []
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error parsing Fireworks Vision AI response: {e}, Content was: {content}")
        return []
        
=======
# backend/core/image_analyzer.py
import requests
import json
import re

# --- NEW, MORE RELIABLE VISION API ENDPOINT ---
# We are switching to the Fireworks.ai hosted LLaVA model.
FIREWORKS_API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"

# NOTE: For a real production app, you would get a free API key from Fireworks.ai
# and include it in the headers for better performance and reliability.
# For this project, we can use their public playground endpoint which doesn't require a key for now.
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer ", # No key needed for this playground model
}

def analyze_product_image(image_url: str):
    """
    Uses a multi-modal AI (LLaVA on Fireworks.ai) to identify materials from a product image.

    Args:
        image_url (str): The public URL of the product image to analyze.

    Returns:
        list: A list of likely materials identified from the image.
    """
    if not image_url:
        return []

    # The prompt remains the same, as it's our core instruction to the AI.
    prompt = """
    Analyze the product in this image. Based on visual cues like texture and reflection,
    what are the most likely primary materials it is made of?
    Return your answer ONLY as a JSON array of lowercase strings.
    Example: ["plastic", "metal", "fabric"]
    """
    
    # The payload structure is different for the Fireworks API.
    payload = {
        "model": "accounts/fireworks/models/llava-v1_6-mistral-7b",
        "max_tokens": 512,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    }

    try:
        print(f"DEBUG: Calling Fireworks Vision AI for image: {image_url}")
        response = requests.post(FIREWORKS_API_URL, headers=HEADERS, json=payload, timeout=45) # Increased timeout
        response.raise_for_status()
        
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        
        # Extract the JSON part from the response string
        json_match = re.search(r'\[.*\]', content)
        if json_match:
            materials = json.loads(json_match.group(0))
            print(f"DEBUG: Vision AI identified materials: {materials}")
            return [str(m).lower() for m in materials] # Ensure all items are lowercase strings

    except requests.exceptions.RequestException as e:
        print(f"Error calling Fireworks Vision AI API: {e}")
        return []
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error parsing Fireworks Vision AI response: {e}, Content was: {content}")
        return []
        
>>>>>>> 2ae3776 (Initial commit for deployment)
    return []
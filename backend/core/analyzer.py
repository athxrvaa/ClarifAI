# backend/core/analyzer.py
import json
from pathlib import Path
from transformers import pipeline
from fastapi import HTTPException

try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    print(f"FATAL: Failed to load Zero-Shot NLP model: {e}")
    classifier = None

def load_lca_data():
    try:
        db_path = Path(__file__).parent.parent / "data" / "lca_database.json"
        with open(db_path, 'r') as f:
            return json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="LCA Database file not found or is invalid.")

LCA_DATA = load_lca_data()
CANDIDATE_MATERIALS = list(LCA_DATA.get("materials", {}).keys())
CANDIDATE_LOCATIONS = list(LCA_DATA.get("manufacturing_locations", {}).keys())
CANDIDATE_BRANDS = list(LCA_DATA.get("brands_origin", {}).keys())
CANDIDATE_CATEGORIES = list(LCA_DATA.get("product_category_inference", {}).keys())

def extract_product_components(description: str, title: str):
    if not classifier:
        raise HTTPException(status_code=500, detail="NLP model is not available.")
    
    full_text = f"{title}. {description}"

    try:
        # 1. Analyze for Materials
        material_results = classifier(full_text, CANDIDATE_MATERIALS, multi_label=True)
        identified_materials = [label for label, score in zip(material_results['labels'], material_results['scores']) if score > 0.60]

        # 2. Analyze for Brand
        brand_results = classifier(title, CANDIDATE_BRANDS, multi_label=False)
        identified_brand = brand_results['labels'][0] if brand_results['scores'][0] > 0.50 else None

        # 3. Analyze for Location (using Brand as the primary signal)
        manufacturing_location = "default"
        if identified_brand and identified_brand in LCA_DATA["brands_origin"]:
            manufacturing_location = LCA_DATA["brands_origin"][identified_brand]
        else: # Fallback to text analysis if brand not found/mapped
            location_results = classifier(full_text, CANDIDATE_LOCATIONS, multi_label=False)
            if location_results['scores'][0] > 0.70:
                manufacturing_location = location_results['labels'][0]

        # 4. Analyze for Product Category
        category_results = classifier(title, CANDIDATE_CATEGORIES, multi_label=False)
        product_category = category_results['labels'][0] if category_results['scores'][0] > 0.80 else None
        
        return {
            "identified_materials": list(set(identified_materials)),
            "manufacturing_location": manufacturing_location,
            "identified_brand": identified_brand,
            "product_category": product_category,
        }

    except Exception as e:
        print(f"Error during NLP analysis: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during NLP analysis.")
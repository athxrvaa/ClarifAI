# backend/core/lca_calculator.py
import json
from pathlib import Path
from .ai_prompts import generate_eol_explanation

def load_lca_data():
    # ... (this function is the same)
    try:
        db_path = Path(__file__).parent.parent / "data" / "lca_database.json"
        with open(db_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

LCA_DATA = load_lca_data()

# --- MODIFIED FUNCTION SIGNATURE ---
def calculate_lca_score(components: dict, vision_materials: list):
    # --- Data Fusion Logic ---
    text_materials = components.get("identified_materials", [])
    inferred_materials = []
    category = components.get("product_category")

    if category and category in LCA_DATA["product_category_inference"]:
        inferred_materials = LCA_DATA["product_category_inference"][category]
    
    # Combine all sources: text, inference, and now vision.
    # Use set() to automatically handle duplicates.
    all_materials = list(set(text_materials + inferred_materials + vision_materials))
    
    # --- The rest of the function is almost identical ---
    manufacturing_location = components.get("manufacturing_location", "default")

    if not all_materials:
        return {
            "final_score": 50,
            "breakdown": {
                "material_carbon_footprint_kgCO2": "N/A", "transportation_carbon_footprint_kgCO2": "N/A",
                "material_water_usage_L": "N/A", "manufacturing_location_factor": "Unknown",
                "end_of_life_score": "N/A",
                "end_of_life_advice": "Could not identify materials for specific disposal advice."
            },
            "summary": "Could not identify materials from text or image. Score is a neutral default."
        }

    # ... (All the calculation logic for carbon, water, eol_score, etc. is exactly the same)
    total_carbon = 0
    total_water = 0
    total_eol_score = 0
    material_db = LCA_DATA.get("materials", {})
    materials_data_for_ai = []
    for mat in all_materials:
        data = material_db.get(mat, {})
        total_carbon += data.get("carbon_kg", 0)
        total_water += data.get("water_l", 0)
        total_eol_score += data.get("eol_score", 5)
        materials_data_for_ai.append({
            "name": mat, "score": data.get("eol_score", 5),
            "recyclability": data.get("recyclability", "unknown"),
            "decomposition": data.get("decomposition", "N/A")
        })
    avg_eol_score = (total_eol_score / len(all_materials)) * 10 if all_materials else 50
    location_db = LCA_DATA.get("manufacturing_locations", {})
    carbon_intensity = location_db.get(manufacturing_location, location_db.get("default", {}))["carbon_intensity_kwh"]
    manufacturing_score = max(0, min(100, (0.8 - carbon_intensity) / 0.6 * 100))
    consumer_location = "India"
    transport_carbon = 0
    long_haul_locations = ["China", "Vietnam", "India"]
    if manufacturing_location in long_haul_locations and manufacturing_location != consumer_location:
        transport_db = LCA_DATA.get("transport", {})
        transport_carbon = transport_db.get("sea_freight_km", 0.015) * 15000 * 1
    total_carbon_with_transport = total_carbon + transport_carbon
    carbon_score = max(0, 100 - (total_carbon_with_transport * 2))
    water_score = max(0, 100 - (total_water / 100))
    weights = {"carbon": 0.5, "water": 0.15, "manufacturing": 0.15, "eol": 0.2}
    final_score = (carbon_score * weights["carbon"]) + (water_score * weights["water"]) + (manufacturing_score * weights["manufacturing"]) + (avg_eol_score * weights["eol"])

    # Update summary to reflect the new data source
    summary_text = f"Analysis based on text, inference, and image analysis. Materials found: {', '.join(all_materials)}. Origin: {manufacturing_location}."
    eol_advice = generate_eol_explanation(materials_data_for_ai)

    return {
        "final_score": round(final_score),
        "breakdown": {
            "material_carbon_footprint_kgCO2": round(total_carbon, 2),
            "transportation_carbon_footprint_kgCO2": round(transport_carbon, 2),
            "material_water_usage_L": round(total_water),
            "manufacturing_location_factor": manufacturing_location,
            "end_of_life_score": round(avg_eol_score),
            "end_of_life_advice": eol_advice
        },
        "summary": summary_text
    }
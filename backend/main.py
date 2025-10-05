<<<<<<< HEAD
# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

from .core.scraper import scrape_product_page
from .core.analyzer import extract_product_components
from .core.lca_calculator import calculate_lca_score
# --- NEW IMPORT ---
from .core.image_analyzer import analyze_product_image

app = FastAPI(
    title="ClarifAI v2: Visual Sustainability Analyzer",
    description="An advanced analyzer that uses both text and image analysis.",
    version="v2.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ProductURL(BaseModel):
    url: HttpUrl

@app.get("/")
def read_root():
    return {"message": "ClarifAI v2 API is running"}

@app.post("/assess")
def assess_product_impact(product: ProductURL):
    try:
        # Step 1: Scrape text AND image URL
        scraped_data = scrape_product_page(str(product.url))
        title = scraped_data.get('product_title', '')
        description = scraped_data.get('product_description', '')
        image_url = scraped_data.get('main_image_url')

        if not title:
            raise HTTPException(status_code=422, detail="Could not extract a product title.")

        # Step 2: Text Analysis (same as before)
        text_components = extract_product_components(description, title)
        
        # --- NEW: Step 3: Vision Analysis ---
        # This runs in parallel to the text analysis.
        vision_identified_materials = analyze_product_image(image_url)
        
        # --- NEW: Step 4: Fuse Data and Calculate Score ---
        # The calculator now receives both sets of materials.
        lca_results = calculate_lca_score(
            components=text_components,
            vision_materials=vision_identified_materials
        )

        return {
            "product_title": title,
            "analysis_results": lca_results,
            "identified_components": text_components,
            "vision_identified_materials": vision_identified_materials
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"UNEXPECTED SERVER ERROR: {e}")
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")

if __name__ == "__main__":
=======
# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

from .core.scraper import scrape_product_page
from .core.analyzer import extract_product_components
from .core.lca_calculator import calculate_lca_score
# --- NEW IMPORT ---
from .core.image_analyzer import analyze_product_image

app = FastAPI(
    title="ClarifAI v2: Visual Sustainability Analyzer",
    description="An advanced analyzer that uses both text and image analysis.",
    version="v2.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ProductURL(BaseModel):
    url: HttpUrl

@app.get("/")
def read_root():
    return {"message": "ClarifAI v2 API is running"}

@app.post("/assess")
def assess_product_impact(product: ProductURL):
    try:
        # Step 1: Scrape text AND image URL
        scraped_data = scrape_product_page(str(product.url))
        title = scraped_data.get('product_title', '')
        description = scraped_data.get('product_description', '')
        image_url = scraped_data.get('main_image_url')

        if not title:
            raise HTTPException(status_code=422, detail="Could not extract a product title.")

        # Step 2: Text Analysis (same as before)
        text_components = extract_product_components(description, title)
        
        # --- NEW: Step 3: Vision Analysis ---
        # This runs in parallel to the text analysis.
        vision_identified_materials = analyze_product_image(image_url)
        
        # --- NEW: Step 4: Fuse Data and Calculate Score ---
        # The calculator now receives both sets of materials.
        lca_results = calculate_lca_score(
            components=text_components,
            vision_materials=vision_identified_materials
        )

        return {
            "product_title": title,
            "analysis_results": lca_results,
            "identified_components": text_components,
            "vision_identified_materials": vision_identified_materials
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"UNEXPECTED SERVER ERROR: {e}")
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")

if __name__ == "__main__":
>>>>>>> 2ae3776 (Initial commit for deployment)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
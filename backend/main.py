# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

# --- Import all necessary modules from the 'core' package ---
from .core.scraper import scrape_product_page
from .core.analyzer import extract_product_components
from .core.lca_calculator import calculate_lca_score
from .core.image_analyzer import analyze_product_image

# --- Initialize the FastAPI application ---
app = FastAPI(
    title="ClarifAI v2: Visual Sustainability Analyzer",
    description="An advanced analyzer that uses both text and image analysis to generate a real-time sustainability score.",
    version="v2.0.0",
)

# --- CORS Middleware Configuration ---
# Allows the browser extension to communicate with this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# --- API Data Models ---
class ProductURL(BaseModel):
    url: HttpUrl

# --- API Endpoints ---

@app.get("/")
def read_root():
    """A simple health-check endpoint to confirm the API is running."""
    return {"message": "ClarifAI v2 API is running and healthy"}


@app.post("/assess")
def assess_product_impact(product: ProductURL):
    """
    The main analysis pipeline. It takes a product URL and returns a comprehensive
    sustainability assessment based on text and visual analysis.
    """
    try:
        # Step 1: Scrape the webpage for text and the main image URL.
        scraped_data = scrape_product_page(str(product.url))
        title = scraped_data.get('product_title', '')
        description = scraped_data.get('product_description', '')
        image_url = scraped_data.get('main_image_url')

        if not title:
            raise HTTPException(status_code=422, detail="Could not extract a product title from the page.")

        # Step 2: Perform text-based analysis to find brand, category, etc.
        text_components = extract_product_components(description, title)
        
        # Step 3: Perform vision-based analysis on the product image.
        vision_identified_materials = analyze_product_image(image_url)
        
        # Step 4: Fuse the data from all sources and calculate the final score.
        lca_results = calculate_lca_score(
            components=text_components,
            vision_materials=vision_identified_materials
        )

        # Step 5: Return the complete analysis to the client.
        return {
            "product_title": title,
            "analysis_results": lca_results,
            "identified_components": text_components,
            "vision_identified_materials": vision_identified_materials
        }
        
    except HTTPException as e:
        # Re-raise known exceptions to send proper error codes.
        raise e
    except Exception as e:
        # Catch any unexpected server errors.
        print(f"UNEXPECTED SERVER ERROR: {e}")
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")


# This block allows running the server directly for local development.
# Render will use the 'Start Command' you provided, not this block.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
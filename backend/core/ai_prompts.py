# backend/core/ai_prompts.py
import os
from groq import Groq

# --- Secure API Key Initialization ---
# This code attempts to read the GROQ_API_KEY from the server's environment variables.
# This is the standard, secure way to handle secret keys.
# The key itself is NOT stored in the code.
try:
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("WARNING: GROQ_API_KEY environment variable not found. AI Narrator features will be disabled.")
        client = None
    else:
        client = Groq(api_key=api_key)

except Exception as e:
    print(f"ERROR: Could not initialize Groq client. AI Narrator will be disabled. Error: {e}")
    client = None


def generate_eol_explanation(materials_data: list):
    """
    Uses a Large Language Model (LLM) to generate a detailed explanation for the End-of-Life score.
    """
    # --- Fallback Logic ---
    # This runs if the Groq client failed to initialize (e.g., key is missing or invalid).
    def get_fallback_tip():
        if not materials_data:
            return "Disposal info unavailable as no materials were identified."
        # Find the material with the worst score to give the most critical advice.
        critical_material = min(materials_data, key=lambda m: m.get('score', 10))
        return f"Key Tip ({critical_material.get('name', 'N/A')}): {critical_material.get('decomposition', 'Follow local recycling guidelines.')}"

    if not client:
        return get_fallback_tip()

    # --- AI Prompt Generation ---
    # Prepare a clean list of materials for the AI to analyze.
    prompt_data = "\n".join([f"- {m.get('name', 'unknown')} (Recyclability: {m.get('recyclability', 'unknown')})" for m in materials_data])
    
    # Calculate the average score to give the AI context.
    avg_score = sum(m.get('score', 5) for m in materials_data) / len(materials_data) * 10 if materials_data else 50
    
    # This is the detailed instruction set for the AI.
    prompt = f"""
    You are a sustainability expert explaining a product's End-of-Life score of {avg_score:.0f}/100.
    The product is made of the following materials:
    {prompt_data}

    Your task is to write a brief, 2-sentence explanation for the user.
    1. In the first sentence, state the main reason for the score (e.g., "This product scores moderately because it's a mix of highly recyclable and non-recyclable parts.").
    2. In the second sentence, give the SINGLE most important piece of disposal advice, focusing on the most problematic material (like e-waste or non-recyclable plastic).
    
    Example for a phone: "The score is low because it contains hazardous e-waste. Critical: The battery must be taken to a designated e-waste facility and not thrown in regular trash."
    Example for a steel bottle: "This scores very high as it's made from infinitely recyclable steel. Advice: Simply ensure it's clean and place it in your metal recycling bin."
    
    Be clear, concise, and helpful.
    """

    try:
        print("DEBUG: Calling Groq API to generate EoL explanation...")
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gemma-7b-it", # Using a stable and capable model
            temperature=0.6,
            max_tokens=100,
        )
        print("DEBUG: Groq API call successful.")
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"ERROR: An error occurred calling Groq API for EoL explanation: {e}")
        # If the API call fails for any reason, return the simple fallback tip.
        return get_fallback_tip()
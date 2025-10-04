# backend/core/ai_prompts.py
from groq import Groq

try:
    client = Groq(
        api_key="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",  # <-- PASTE YOUR KEY HERE
    )
except Exception:
    client = None

def generate_eol_explanation(materials_data: list):
    """
    Uses an LLM to generate a detailed explanation for the End-of-Life score.
    """
    if not client:
        # Provide a simple, non-AI fallback
        if not materials_data:
            return "Disposal info unavailable."
        critical_material = min(materials_data, key=lambda m: m['score'])
        return f"Key Tip ({critical_material['name']}): {critical_material['decomposition']}"

    # Prepare the data for the prompt
    prompt_data = "\n".join([f"- {m['name']} (Recyclability: {m['recyclability']})" for m in materials_data])
    
    # Calculate the average score to give the AI context
    avg_score = sum(m['score'] for m in materials_data) / len(materials_data) * 10 if materials_data else 50
    
    prompt = f"""
    You are a sustainability expert explaining a product's End-of-Life score of {avg_score:.0f}/100.
    The product is made of the following materials:
    {prompt_data}

    Your task is to write a brief, 2-sentence explanation for the user.
    1. In the first sentence, state the main reason for the score (e.g., "This product scores moderately because it's a mix of highly recyclable and non-recyclable parts.").
    2. In the second sentence, give the SINGLE most important piece of disposal advice, focusing on the most problematic material (like e-waste or non-recyclable plastic).
    
    Example for a phone: "The score is low because it contains e-waste. Critical: The battery must be taken to an e-waste facility and not thrown in the trash."
    Example for a steel bottle: "This scores very high as it's made from infinitely recyclable steel. Advice: Simply place it in your metal recycling bin."
    
    Be clear and concise.
    """

    try:
        print("DEBUG: Calling Groq API with the new model...")
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.6,
            max_tokens=100,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling Groq API for EoL explanation: {e}")
        # Fallback to the simple summary if the API call fails
        critical_material = min(materials_data, key=lambda m: m['score'])
        return f"Key Tip ({critical_material['name']}): {critical_material['decomposition']}"
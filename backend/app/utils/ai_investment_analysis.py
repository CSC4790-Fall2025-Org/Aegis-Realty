import json
from ..core.prompts import generate_investment_prompt
from ..core.config import settings

# Defer importing google.genai until we actually need to call it. This avoids
# raising exceptions at import time when API keys or Google client configuration
# are not present (e.g., during local static checks or quick imports).
def _create_genai_client():
    try:
        from google import genai
        from google.genai import types
    except Exception:
        return None, None

    api_key = settings.GOOGLE_GENAI_KEY
    if not api_key:
        return None, None

    genai.api_key = api_key
    client = genai.Client(api_key=api_key)
    return client, types


def ai_investment_analysis(property_data, cap_rate):
    """Generate an AI investment analysis. If the GenAI client or API key is
    not configured, return a safe fallback dict rather than raising at import
    time.
    """
    client, types = _create_genai_client()
    prompt = generate_investment_prompt(property_data, cap_rate)

    if client is None:
        # Return a harmless placeholder so the calling code can continue to
        # operate (useful for local development and tests).
        return {"investment_analysis": {"note": "Google GenAI not configured; skipping AI analysis."}}

    res = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a professional real estate investment analyst"
        ),
        contents=prompt
    )

    text = res.candidates[0].content.parts[0].text
    try:
        investment_analysis_json = json.loads(text)
    except Exception as e:
        raise ValueError(f"Failed to parse Gemini output as JSON. Error: {e}\nRaw output:\n{text}")
    return {"investment_analysis": investment_analysis_json}
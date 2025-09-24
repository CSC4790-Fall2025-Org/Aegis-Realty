from google import genai
import json
from prompts import generate_investment_prompt
from google.genai import types
from .config import settings

api_key = settings. GOOGLE_GENAI_KEY
genai.api_key = api_key

client = genai.Client(api_key=api_key,)

def ai_investment_analysis(property_data, roi, cap_rate):
    prompt = generate_investment_prompt(property_data, roi, cap_rate)
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
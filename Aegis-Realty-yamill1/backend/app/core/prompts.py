def generate_investment_prompt(property_data, cap_rate):
    return f"""
    You are a real estate investment analyst. Your task is to provide a comprehensive analysis of a property based on the provided data.

    Property Data:
    {property_data}

    Key Metrics:
    - Capitalization Rate (Cap Rate): {cap_rate}%

    Instructions:
    1.  **Summary of the Property:** Provide a brief, professional summary of the property and its key features.
    2.  **Investment Recommendation:** Based on the provided Cap Rate, give a clear decision on whether this is a good investment. Justify your decision with a short explanation.
    3.  **Potential Risks:** Identify any potential risks or red flags that an investor should be aware of, based on the property data.
    4.  **Recommendations:** Offer a few recommendations on how an investor could improve the property's value or increase its rental income.

    Output formatting:
    - The output must be pure, raw JSON.
    - Do not return the JSON wrapped in quotes or with escaped characters like \n or ".
    - Do not include any Markdown, plain text, explanations, commentary, or symbols like asterisks or hash signs.
    - Do not wrap the JSON in markdown-style code blocks (e.g., triple backticks ``` or ```json).
    - Format must be valid and parseable by standard JSON parsers.
    - The JSON object should have the following structure:
    {{
        "summary": "...",
        "recommendation": {{
            "decision": "Invest" or "Do Not Invest",
            "justification": "..."
        }},
        "potential_risks": [
            "...",
            "...",
            "..."
        ],
        "recommendations": [
            "...",
            "...",
            "..."
        ]
    }}

    If you cannot provide the requested information, respond with an empty JSON object.
    Start your response with {{ and end with }}. Nothing else.
    """
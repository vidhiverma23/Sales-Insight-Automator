"""AI Engine service: generates professional sales summaries using Google Gemini."""

import google.generativeai as genai
from app.config import get_settings


SYSTEM_PROMPT = """You are a senior business analyst at a Fortune 500 company. 
Your task is to generate a professional, executive-ready sales brief from raw data.

Your summary MUST include:
1. **Executive Summary** — A 2-3 sentence high-level overview of the data.
2. **Key Metrics** — The most important numbers (revenue, growth, top products, etc.).
3. **Trends & Insights** — Notable patterns, year-over-year changes, seasonal effects.
4. **Actionable Recommendations** — 3-5 concrete next steps based on the data.

Format the output as clean HTML suitable for an email. Use headers, bold text, and 
bullet points for readability. Keep the tone professional yet concise.
Do NOT include ```html or ``` markdown fences — output raw HTML only."""


async def generate_summary(data_text: str) -> str:
    """
    Send parsed data to Gemini and return a professional HTML summary.
    
    Args:
        data_text: Structured text representation of the sales data.
    
    Returns:
        HTML-formatted sales brief.
    """
    settings = get_settings()

    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured. Set it in your .env file.")

    genai.configure(api_key=settings.GEMINI_API_KEY)

    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    prompt = f"""{SYSTEM_PROMPT}

Here is the raw sales data to analyze:

{data_text}

Generate the executive sales brief now."""

    response = model.generate_content(prompt)
    
    return response.text

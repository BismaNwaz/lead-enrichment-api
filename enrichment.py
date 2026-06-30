import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

EXTRACTION_PROMPT = """You are analyzing a company's website content to extract structured business information.

Website content:
{content}

Extract the following as JSON only, no other text:
{{
  "company_name": "",
  "industry": "",
  "summary": "2-3 sentence description of what the company does",
  "products_or_services": [],
  "likely_decision_maker_titles": [],
  "contact_email": "",
  "location": ""
}}

If a field cannot be determined, use null."""

def enrich_company_data(website_text: str) -> dict:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": EXTRACTION_PROMPT.format(content=website_text)}
        ]
    )
    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
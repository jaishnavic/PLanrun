import json
import re
import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# Load environment variables
load_dotenv()

# Read API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=GEMINI_API_KEY)

# 🔹 SYSTEM PROMPT FOR SUPPLY PLAN RUNS
SYSTEM_PROMPT = """
You are an Oracle Fusion Supply Planning assistant.

Your task:
- Identify whether the user wants to RUN a supply plan
- Identify the execution mode

You MUST return ONLY valid JSON.
Do NOT add explanations or extra text.

Valid intent:
- RUN_SUPPLY_PLAN

Valid mode_label values:
- SIMULATION
- REPLAN
- FULL
- DEFAULT

Rules:
- "simulation" → SIMULATION
- "replan" → REPLAN
- "full" → FULL
- If mode is not clearly mentioned → DEFAULT
- If the user intent is unclear, still assume RUN_SUPPLY_PLAN

Response format (ALWAYS):
{
  "intent": "RUN_SUPPLY_PLAN",
  "mode_label": "DEFAULT"
}
"""


def call_llm(user_prompt: str) -> dict:
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser input:\n{user_prompt}"
        )

        raw_text = response.text.strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                return json.loads(match.group())

        return {
            "intent": "ERROR",
            "error": "Invalid JSON returned by LLM"
        }

    except ClientError as e:
        # 🔥 HANDLE GEMINI QUOTA / RATE LIMIT
        if e.status_code == 429:
            return {
                "intent": "ERROR",
                "error_type": "LLM_QUOTA_EXCEEDED",
                "message": "LLM quota exceeded. Please try again later."
            }

        return {
            "intent": "ERROR",
            "error_type": "LLM_CLIENT_ERROR",
            "message": str(e)
        }

    except Exception as e:
        return {
            "intent": "ERROR",
            "error_type": "LLM_UNKNOWN_ERROR",
            "message": str(e)
        }

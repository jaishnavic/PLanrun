import json
import re
import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=GEMINI_API_KEY)

# 🔹 SYSTEM PROMPT FOR SUPPLY PLAN ACTIONS
SYSTEM_PROMPT = """
You are an Oracle Fusion Supply Planning assistant.

Your task:
- Identify the user's intent related to supply plans
- Identify execution mode ONLY if the intent is RUN_SUPPLY_PLAN

Valid intents:
- RUN_SUPPLY_PLAN
- CREATE_RELEASE_PLAN

Valid mode_label values (ONLY for RUN_SUPPLY_PLAN):
- SIMULATION
- REPLAN
- FULL
- DEFAULT

Rules:
- If user asks to run / execute / start a plan → RUN_SUPPLY_PLAN
- If user asks to create / generate / publish a release → CREATE_RELEASE_PLAN

Mode rules (RUN_SUPPLY_PLAN only):
- "simulation" → SIMULATION
- "replan" → REPLAN
- "full" → FULL
- If not mentioned → DEFAULT

For CREATE_RELEASE_PLAN:
- Do NOT infer mode
- Always return mode_label as null

Return ONLY valid JSON.
Do NOT add explanations or extra text.

Response formats:

RUN PLAN:
{
  "intent": "RUN_SUPPLY_PLAN",
  "mode_label": "DEFAULT"
}

CREATE RELEASE:
{
  "intent": "CREATE_RELEASE_PLAN",
  "mode_label": null
}
"""


def call_llm(user_prompt: str) -> dict:
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser input:\n{user_prompt}"
        )

        raw_text = response.text.strip()

        # 🔐 HARDEN JSON PARSING
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                return json.loads(match.group())

        return {
            "intent": "ERROR",
            "error": "Invalid JSON returned by LLM",
            "raw_output": raw_text
        }

    except ClientError as e:
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

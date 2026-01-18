import os
import json
from fastapi import HTTPException
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# ================= ENV =================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

# ================= JSON SAFETY =================
def safe_json_parse(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(text[start:end])
    raise HTTPException(500, "Invalid JSON from AI")

# ================= CORE =================
def chatbot(input_text: str) -> dict:
    try:
        model = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=GROQ_API_KEY,
            temperature=0,
            max_tokens=700,
            timeout=60,
            response_format={"type": "json_object"},  # 🔥 CRITICAL
        )

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a local salon discovery assistant. "
                "Return top 10 salons near the given location. "
                "Respond ONLY with valid JSON."
            ),
            (
                "user",
                """
Location: {text}

Return JSON exactly in this format:
{{
  "results": [
    {{
      "name": "string",
      "address": "string",
      "phone": "string or empty",
      "rating": "string",
      "map_url": "string"
    }}
  ]
}}
"""
            )
        ])

        chain = prompt | model | StrOutputParser()

        raw = chain.invoke({"text": input_text})

        return json.loads(raw)  # ✅ WILL NOT FAIL NOW

    except Exception as e:
        print("❌ GROQ ERROR:", repr(e))
        raise HTTPException(
            status_code=503,
            detail="Groq AI service unavailable"
        )

# controller.py
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from kb_loader import load_kb, search_kb

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Choose a working Gemini model
MODEL = "gemini-2.5-flash"  

KB = load_kb("knowledge_base_txt")
ACTOR_API_URL = os.getenv("ACTOR_API_URL")

def ask_agent(query: str):
    # 1. Try KB first
    kb_answer = search_kb(KB, query)
    if kb_answer:
        return {
            "query": query,
            "answer": kb_answer[:500],  # trim long text
            "source": "knowledge_base"
        }

    # 2. If not in KB, call Actor API (REST)
    try:
        resp = requests.get(f"{ACTOR_API_URL}/info/{query}")
        if resp.status_code == 200 and "error" not in resp.json():
            return {
                "query": query,
                "answer": resp.json()["answer"],
                "source": "actor_api"
            }
    except Exception as e:
        print("Actor API error:", e)

    # 3. If not in KB or Actor, fallback to Gemini API
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(query)

    return {
        "query": query,
        "answer": response.text,
        "source": "gemini_api"
    }
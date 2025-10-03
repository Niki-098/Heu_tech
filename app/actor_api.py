from fastapi import FastAPI
from app.kb_loader import load_kb, search_kb
import google.generativeai as genai
import os
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load docs once
docs = load_kb("knowledge_base_txt")  # Update to match your directory if needed

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/info/{topic}")
async def get_info(topic: str):
    logger.info(f"Received query: {topic}")
    # Try KB first
    kb_answer = search_kb(docs, topic, min_score=0.3)  # Use similarity threshold
    logger.info(f"KB search for '{topic}': {'Found' if kb_answer else 'Not found'}")
    
    if kb_answer and kb_answer.strip():
        # Summarize KB text via Gemini if valid content is found
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = f"Summarize the following text in response to the query: '{topic}'. If the text is irrelevant to the query, explicitly state that no relevant information was found and do not provide a summary.\n\nText: {kb_answer[:2000]}"  # Truncate if too long
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            # Check if response indicates no relevant information
            if "no relevant information" in response_text.lower() or not response_text:
                logger.warning(f"KB content for '{topic}' is irrelevant or empty summary")
                # Fall back to direct Gemini query
                response = model.generate_content(topic)
                return {"answer": response.text, "source": "gemini_api"}
            return {"answer": response_text, "source": "knowledge_base_summarized"}
        except Exception as e:
            logger.error(f"Gemini error during KB summarization: {e}")
            # Fall back to direct Gemini query on error
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(topic)
                return {"answer": response.text, "source": "gemini_api"}
            except Exception as e2:
                logger.error(f"Gemini error for direct query: {e2}")
                return {"error": str(e2), "source": "gemini_api"}
    else:
        # Use Gemini directly if no KB match
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(topic)
            return {"answer": response.text, "source": "gemini_api"}
        except Exception as e:
            logger.error(f"Gemini error for direct query: {e}")
            return {"error": str(e), "source": "gemini_api"}
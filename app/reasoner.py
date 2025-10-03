# reasoner.py
import google.generativeai as genai
import os

class Reasoner:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def reason(self, query, context):
        prompt = f"""
        You are an AI agent.
        Context from KB: {context}
        Question: {query}
        If the context contains relevant information to answer the question, use it to provide a concise, summarized answer.
        If the context is irrelevant or insufficient, return exactly: "API_CALL: {query}"
        """
        response = self.model.generate_content(prompt)
        return response.text
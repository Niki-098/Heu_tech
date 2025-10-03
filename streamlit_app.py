import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8001/info"

st.set_page_config(page_title="AI Reasoner", page_icon="🤖", layout="centered")

st.title("🤖 Ask AI Anything (Gemini + FastAPI)")
st.write("Type a topic or question to get an AI-powered explanation from the knowledge base or Gemini API.")

# Input box
topic = st.text_input("Enter a topic or question:", placeholder="e.g., What is data preprocessing?")

# Button
if st.button("Get Answer"):
    if topic.strip():
        with st.spinner("Fetching answer..."):
            try:
                response = requests.get(f"{API_URL}/{topic}")
                if response.status_code == 200:
                    data = response.json()
                    if "answer" in data and data["answer"].strip():
                        st.subheader("Answer:")
                        st.success(data["answer"])
                        st.subheader("Source:")
                        source = data.get("source", "Unknown")
                        if source == "knowledge_base_summarized":
                            st.info("Retrieved from Knowledge Base (summarized by Gemini)")
                        elif source == "gemini_api":
                            st.info("Retrieved directly from Gemini API")
                        else:
                            st.warning(f"Unknown source: {source}")
                    elif "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        st.error("No valid answer received from the server.")
                else:
                    st.error(f"HTTP Error: {response.status_code} - Failed to connect to the server.")
            except Exception as e:
                st.error(f"Request failed: {e}. Please ensure the FastAPI server is running on port 8001.")
    else:
        st.warning("Please enter a topic or question.")
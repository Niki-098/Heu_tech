# AI Reasoner with Knowledge Base and Gemini API
This project implements a Retrieval-Augmented Generation (RAG) system that answers user queries by searching a local knowledge base (KB) of text files or falling back to Google's Gemini API. The system uses a Streamlit frontend, a FastAPI backend, and Sentence Transformers for semantic search. It supports two modes: a direct query via Streamlit and a pipeline mode with PDF-based retrieval.


## Project Structure

**streamlit_app.py:** Streamlit frontend for user interaction.<br>
**actor_api.py:** FastAPI server handling KB search and Gemini API calls.<br>
**kb_loader.py:** Loads and searches the KB (TXT files) using Sentence Transformers.<br>
**controller.py:** Manages query flow for the Streamlit mode.<br>
**main.py:** Runs the pipeline mode with PDF retrieval.<br>
**retriever.py:** Handles PDF-based retrieval with FAISS.<br>
**reasoner.py:** Uses Gemini to reason over retrieved context.<br>
**actor.py:** Makes API calls to the FastAPI server.<br>
**knowledge_base_txt/:** Directory for TXT files (converted from PDFs).<br>
**knowledge_base/:** Directory for PDF files (used in pipeline mode).<br>

## Setup Instructions
### Prerequisites

Python 3.8+<br>
A Google API key for Gemini (set in .env)<br>
Install dependencies:pip install streamlit fastapi uvicorn python-dotenv sentence-transformers google-generativeai faiss-cpu PyPDF2<br>



## Installation

Clone the Repository:<br>
git clone <repository-url><br>
cd <repository-directory><br>


## Set Up Environment Variables:

Create a .env file in the project root:GEMINI_API_KEY=your_google_api_key<br>
ACTOR_API_URL=http://127.0.0.1:8001<br><br>


Replace your_google_api_key with a valid Google API key.


## Prepare Knowledge Base:

Place TXT files (converted from PDFs) in knowledge_base_txt/.<br>
Example file (data_preprocessing.txt):Data preprocessing is the process of cleaning and transforming raw data to prepare it for machine learning models...<br><br>


### For pipeline mode, place PDFs in knowledge_base/.


Run the FastAPI Server:<br>
uvicorn app.actor_api:app --host 127.0.0.1 --port 8001<br><br>


Ensure port 8001 is free; use 8002 if needed (update .env, actor.py, streamlit_app.py).


#### Run the Streamlit App:
streamlit run streamlit_app.py<br>

Open http://localhost:8501 in your browser.


Run the backend:<br>
uvicorn app.actor_api:app --reload --port 8001<br><br>


Tests queries using PDF-based retrieval.<br>



## Usage

### Streamlit Mode:
Enter a query (e.g., "what is data preprocessing") in the Streamlit app.<br>
The system searches knowledge_base_txt/, summarizes with Gemini if relevant, or falls back to Gemini directly.<br>
Response includes the answer and source (knowledge_base_summarized or gemini_api).<br>


### Pipeline Mode:
Run main.py to process queries using PDF retrieval with FAISS, reasoning, and API fallback.



## Design Decisions

### RAG Architecture:

Combines a local KB with Gemini API for accurate, context-aware answers.<br>
TXT-based KB for Streamlit mode (simpler) and PDF-based for pipeline mode (more robust).<br>


### Semantic Search:

Uses multi-qa-MiniLM-L6-cos-v1 Sentence Transformer for query-document matching.<br>
Chunks TXT files by paragraphs to improve relevance.<br>
Added min_score=0.3 threshold to filter irrelevant KB matches.<br>


### Source Tracking:

Responses include a source field (knowledge_base_summarized or gemini_api) for transparency.<br>
Gemini summarizes KB content when relevant; otherwise, it answers directly.<br>


### FastAPI and Streamlit:

FastAPI handles API requests efficiently.<br>
Streamlit provides a user-friendly interface with clear answer and source display.<br>


### Logging:

Extensive logging in actor_api.py and kb_loader.py to debug KB loading and search results.<br>



### Known Limitations

**KB Relevance:**

If knowledge_base_txt/ lacks relevant content, the system falls back to Gemini, but early versions incorrectly labeled irrelevant KB matches as knowledge_base_summarized.<br> Fixed with similarity threshold and response checks.<br>
Whole-paragraph chunking may miss fine-grained matches; smaller chunks could improve accuracy.<br>


**Model Availability:**

The gemini-2.5-flash model caused errors due to API version issues. Switched to gemini-1.5-flash-latest for stability, but users must verify model availability with genai.list_models().


**Connection Issues:**

[WinError 10061] errors occur if the FastAPI server isn’t running or port 8001 is blocked. Users must ensure the server is active and check port availability.


**KB Setup:**

Requires manual conversion of PDFs to TXT for knowledge_base_txt/. Automated conversion could streamline setup.<br>
Empty or irrelevant KB leads to Gemini fallback, which may increase API usage.<br>


**Pipeline vs. Streamlit:**

Pipeline mode uses PDFs with FAISS, while Streamlit uses TXT files, causing potential inconsistency. Future versions could unify KB formats.



### Troubleshooting

**Model Error:** Run the following to check available models:<br>
*import google.generativeai as genai<br>
from dotenv import load_dotenv<br>
import os<br>
load_dotenv()<br>
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))<br>
for model in genai.list_models():<br>
    print(model.name, model.supported_generation_methods)*<br><br>


Update actor_api.py, reasoner.py, and controller.py with a supported model (e.g., gemini-pro).


**Connection Error:** Check port 8001:<br>
netstat -a -n -o | find "8001"<br><br>


Switch to 8002 if blocked.


**KB Issues:** Verify knowledge_base_txt/ contents:<br>
dir knowledge_base_txt<br><br>


Add relevant .txt files and check FastAPI logs for KB search for '<query>': Found/Not found.<br><br>



# Loom video link 

https://www.loom.com/share/8f450a84890240d087d1c4ca2074ab51?sid=97b7a6ca-c7b7-4330-8700-247e1e66c2c4

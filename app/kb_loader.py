from sentence_transformers import SentenceTransformer, util
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load embedding model once
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")  # Updated to a more query-focused model

# Load docs at startup
def load_kb(kb_path="knowledge_base"):
    docs = []
    for filename in os.listdir(kb_path):
        if filename.endswith(".txt"):
            with open(os.path.join(kb_path, filename), "r", encoding="utf-8") as f:
                text = f.read()
                chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]  # Split by paragraphs
                docs.extend(chunks)
    logger.info(f"Loaded {len(docs)} documents from {os.path.abspath(kb_path)}: {os.listdir(kb_path)}")
    return docs

def search_kb(docs, query, top_k=1, min_score=0.3):
    if not docs:
        logger.info("No documents in KB")
        return None
    doc_embeddings = model.encode(docs, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, doc_embeddings, top_k=top_k)
    if not hits or not hits[0] or hits[0][0]["score"] < min_score:
        logger.info(f"No KB match for '{query}' with score >= {min_score}")
        return None
    best_idx = hits[0][0]["corpus_id"]
    logger.info(f"KB match found for '{query}' with score {hits[0][0]['score']}")
    return docs[best_idx]
# retriever.py
import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import numpy as np

class Retriever:
    def __init__(self, kb_path="knowledge_base", index_file="vector.index"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.kb_path = kb_path
        self.index_file = index_file
        self.index, self.docs = self._load_or_build_index()

    def _load_docs(self):
        docs = []
        for file in os.listdir(self.kb_path):
            if file.endswith(".pdf"):
                reader = PdfReader(os.path.join(self.kb_path, file))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + " "
                docs.append((file, text))
        print(f"Loaded {len(docs)} PDF documents from {os.path.abspath(self.kb_path)}: {os.listdir(self.kb_path)}")
        return docs

    def _load_or_build_index(self):
        if os.path.exists(self.index_file) and os.path.exists("docs.pkl"):
            index = faiss.read_index(self.index_file)
            with open("docs.pkl", "rb") as f:
                docs = pickle.load(f)
            return index, docs

        docs = self._load_docs()
        embeddings = [self.model.encode(text) for _, text in docs]
        dim = len(embeddings[0])
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings).astype("float32"))

        faiss.write_index(index, self.index_file)
        with open("docs.pkl", "wb") as f:
            pickle.dump(docs, f)

        return index, docs

    def search(self, query, k=2):
        q_emb = self.model.encode(query).reshape(1, -1)
        D, I = self.index.search(q_emb, k)
        results = [self.docs[i] for i in I[0]]
        return results
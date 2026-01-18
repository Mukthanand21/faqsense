from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os


class FAQRetriever:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.faqs = []
        self.embeddings = None

    def build_index(self, faqs):
        """
        Build FAISS index from FAQ data.
        Combine question and answer into chunks.
        """
        self.faqs = faqs
        chunks = [
            f"Question: {faq['question']} Answer: {faq['answer']}" for faq in faqs
        ]
        self.embeddings = self.model.encode(chunks)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

    def search(self, query, top_k=3):
        """
        Search for top-k similar FAQs.
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        query_emb = self.model.encode([query])
        faiss.normalize_L2(query_emb)
        distances, indices = self.index.search(query_emb, top_k)
        results = [self.faqs[i] for i in indices[0] if i < len(self.faqs)]
        return results, distances[0]

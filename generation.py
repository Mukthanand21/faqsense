from groq import Groq
import os


class FAQGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate_answer(self, query, retrieved_faqs):
        """
        Generate answer using Groq API, based on retrieved FAQs.
        """
        if not retrieved_faqs:
            return "I'm sorry, but I couldn't find an answer to your question in the provided FAQ data."

        context = "\n".join(
            [f"Q: {faq['question']}\nA: {faq['answer']}" for faq in retrieved_faqs]
        )

        prompt = f"""
You are an FAQ assistant. Answer the user's question using ONLY the provided FAQ context below.
Do NOT use external knowledge. If the question cannot be answered from the context, say so.

Context:
{context}

User Question: {query}

Answer concisely and clearly:
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fast model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0,  # Deterministic
        )

        return response.choices[0].message.content.strip()

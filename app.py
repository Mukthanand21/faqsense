import streamlit as st
from data_ingestion import load_faq_data
from retrieval import FAQRetriever
from generation import FAQGenerator
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


# Security fix: API key from environment only
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error(
        "Missing GROQ_API_KEY environment variable. Please set it and restart the app."
    )
    st.stop()

st.title("FAQSense")
st.write("Upload an FAQ file and ask questions to get accurate, AI-powered answers.")

uploaded_file = st.file_uploader(
    "Upload FAQ file (CSV, JSON, or TXT)", type=["csv", "json", "txt"]
)

if uploaded_file:
    try:
        # Fix: Handle CSV directly with pandas; others via temp file
        file_ext = uploaded_file.name.split(".")[-1].lower()
        if file_ext == "csv":
            # Read CSV directly from uploaded file
            df = pd.read_csv(uploaded_file)
            # Check for required columns (case-insensitive)
            columns_lower = [col.lower() for col in df.columns]
            if "question" not in columns_lower or "answer" not in columns_lower:
                st.error(
                    "CSV file must contain 'question' and 'answer' columns (case-insensitive)."
                )
                st.stop()
            # Normalize columns to lowercase and extract
            df.columns = columns_lower
            faqs = df[["question", "answer"]].to_dict("records")
        elif file_ext in ["json", "txt"]:
            # Use existing logic for JSON and TXT
            with open("temp_faq_file", "wb") as f:
                f.write(uploaded_file.getbuffer())
            faqs = load_faq_data("temp_faq_file")
            os.remove("temp_faq_file")
        else:
            st.error("Unsupported file format. Please upload CSV, JSON, or TXT.")
            st.stop()

        st.success(f"Loaded {len(faqs)} FAQs.")

        # Build retriever (preserve RAG logic)
        retriever = FAQRetriever()
        retriever.build_index(faqs)

        # Generator
        generator = FAQGenerator(groq_api_key)

        # User question input
        query = st.text_input("Enter your question:")

        if query:
            with st.spinner("Retrieving and generating answer..."):
                # Retrieval
                retrieved, scores = retriever.search(query, top_k=3)

                # Generation
                answer = generator.generate_answer(query, retrieved)

                # Display answer
                st.subheader("Answer:")
                st.write(answer)

                # Show sources
                st.subheader("Sources:")
                for i, faq in enumerate(retrieved):
                    with st.expander(f"Source {i + 1} (Similarity: {scores[i]:.2f})"):
                        st.write(f"**Question:** {faq['question']}")
                        st.write(f"**Answer:** {faq['answer']}")

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        if os.path.exists("temp_faq_file"):
            os.remove("temp_faq_file")

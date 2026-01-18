import streamlit as st
from data_ingestion import load_faq_from_uploaded_file
from retrieval import FAQRetriever
from generation import FAQGenerator
import os

# ===============================
# ENV CHECK
# ===============================
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("Missing GROQ_API_KEY environment variable. Please set it and restart the app.")
    st.stop()

# ===============================
# SESSION STATE INIT (CRITICAL FIX)
# ===============================
if "faqs" not in st.session_state:
    st.session_state.faqs = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "generator" not in st.session_state:
    st.session_state.generator = None

# ===============================
# HERO HEADER
# ===============================
st.markdown("""
<div style="text-align: center; padding: 20px;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="margin: 0; font-size: 3em;">FAQSense</h1>
    <p style="margin: 10px 0; font-size: 1.2em;">AI-Powered FAQ Assistant</p>
    <span style="background: rgba(255,255,255,0.2);
    padding: 5px 10px; border-radius: 20px; font-size: 0.9em;">
        RAG-Powered
    </span>
</div>
""", unsafe_allow_html=True)

st.write("Upload FAQ files and ask questions to get accurate answers.")

# ===============================
# SIDEBAR NAVIGATION (DROPDOWN)
# ===============================
with st.sidebar:
    st.markdown("## FAQSense")
    page = st.selectbox(
        "Navigate",
        ["📁 Upload FAQs", "❓ Ask Questions", "ℹ️ About"],
    )

# Map dropdown to page key
if page == "📁 Upload FAQs":
    page_key = "upload"
elif page == "❓ Ask Questions":
    page_key = "ask"
else:
    page_key = "about"

# ===============================
# PAGE: UPLOAD
# ===============================
if page_key == "upload":
    st.markdown("**Step 1:** Upload one or more FAQ files (CSV, JSON, or TXT).")
    st.divider()

    uploaded_files = st.file_uploader(
        "Select CSV, JSON, or TXT files",
        type=["csv", "json", "txt"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        faqs = []
        for uploaded_file in uploaded_files:
            try:
                faqs.extend(load_faq_from_uploaded_file(uploaded_file))
            except Exception as e:
                st.error(f"Error in file '{uploaded_file.name}': {str(e)}")

        if faqs:
            st.success(f"Loaded {len(faqs)} FAQs from {len(uploaded_files)} files.")

            # Store in session state (IMPORTANT)
            st.session_state.faqs = faqs
            st.session_state.retriever = FAQRetriever()
            st.session_state.retriever.build_index(faqs)
            st.session_state.generator = FAQGenerator(groq_api_key)

            st.markdown("""
            <div style="margin-top:16px; padding:16px;
            background:#ecfdf5; border-left:5px solid #10b981;
            border-radius:10px; color:#065f46;">
                <strong>✅ Knowledge Base Ready</strong><br>
                You can now ask questions in the <em>Ask Questions</em> section.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("No valid FAQs loaded.")

# ===============================
# PAGE: ASK (FIXED)
# ===============================
elif page_key == "ask":
    # if not st.session_state.faqs:
    if (
        st.session_state.faqs is None
        or st.session_state.retriever is None
        or st.session_state.generator is None
):
        st.info("Please upload FAQ files first.")
    else:
        st.markdown("**Step 2:** Ask a question based on the uploaded FAQs.")
        st.divider()

        query = st.text_input(
            "Enter your question:",
            placeholder="e.g., How can I activate SBI internet banking?",
            key="user_query"
        )

        if query:
            with st.spinner("Retrieving and generating answer..."):
                retrieved, scores = st.session_state.retriever.search(query, top_k=3)
                answer = st.session_state.generator.generate_answer(query, retrieved)

            # ANSWER (VISIBILITY FIXED)
            st.header("💡 Answer")
            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid #4CAF50;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    margin: 15px 0;
                    color: #111827;
                    font-size: 1.2em;
                    line-height: 1.5;
                ">
                    {answer}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.header("📚 Sources")
            for i, faq in enumerate(retrieved[:3]):
                with st.expander(f"Source {i + 1} (Similarity: {scores[i]:.2f})"):
                    st.write(f"**Question:** {faq['question']}")
                    st.write(f"**Answer:** {faq['answer']}")

# ===============================
# PAGE: ABOUT
# ===============================
elif page_key == "about":
    st.subheader("What FAQSense Does")
    st.write(
        "FAQSense is an AI-powered FAQ assistant that uses Retrieval-Augmented "
        "Generation (RAG) to provide accurate answers strictly from uploaded FAQ data."
    )

    st.subheader("Why RAG?")
    st.write(
        "RAG retrieves the most relevant FAQ entries first and generates answers "
        "grounded only in that retrieved content."
    )

    st.subheader("Trustworthy Answers")
    st.write(
        "Answers come only from the uploaded FAQs, ensuring accuracy and "
        "preventing hallucinations."
    )

# ===============================
# FOOTER
# ===============================
st.divider()
st.markdown("""
---
**FAQSense** – AI-powered FAQ Assistant using Retrieval-Augmented Generation (RAG)
""")

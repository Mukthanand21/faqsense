import streamlit as st
import os

from data_ingestion import (
    load_faq_from_uploaded_file,
    load_faq_from_path,
)
from retrieval import FAQRetriever
from generation import FAQGenerator

# ===============================
# ENV CHECK
# ===============================
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("Missing GROQ_API_KEY environment variable.")
    st.stop()

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="FAQSense",
    layout="wide",
)

# ===============================
# HERO HEADER
# ===============================
st.markdown(
    """
<div style="text-align:center; padding:24px;
background:linear-gradient(135deg,#667eea,#764ba2);
color:white; border-radius:14px; margin-bottom:24px;">
    <h1 style="margin:0;">FAQSense</h1>
    <p style="margin:6px 0;">RAG-powered Smart FAQ Assistant</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===============================
# DATASET DISCOVERY
# ===============================
DATASET_DIR = "datasets"


def get_dataset_categories():
    if not os.path.exists(DATASET_DIR):
        return []
    return [
        os.path.splitext(f)[0]
        for f in os.listdir(DATASET_DIR)
        if f.endswith((".csv", ".json", ".txt"))
    ]


DATASET_CATEGORIES = get_dataset_categories()

# ===============================
# CACHE CATEGORY RESOURCES
# ===============================
@st.cache_resource
def load_category_resources(file_path):
    faqs = load_faq_from_path(file_path)
    retriever = FAQRetriever()
    retriever.build_index(faqs)
    generator = FAQGenerator(groq_api_key)
    return faqs, retriever, generator

# ===============================
# SIDEBAR NAVIGATION
# ===============================
with st.sidebar:
    st.markdown("## Navigation")
    section = st.selectbox(
        "Choose Section",
        ["🏠 Home", "📂 FAQ Categories", "⬆️ Upload FAQs"],
    )

# ===============================
# HOME PAGE
# ===============================
if section == "🏠 Home":
    st.header("Welcome to FAQSense 👋")

    st.markdown(
        """
### How to use FAQSense

#### 🔹 Option 1: FAQ Categories
1. Go to **FAQ Categories**
2. Select a category (auto-loaded from datasets)
3. Ask your question

#### 🔹 Option 2: Upload FAQs
1. Upload your CSV / JSON / TXT file
2. Ask questions from your own dataset

---

### Why FAQSense?
- Uses **Retrieval-Augmented Generation (RAG)**
- Answers come **only from your data**
- No hallucinations
- Fast & accurate
"""
    )

# ===============================
# FAQ CATEGORIES MODE
# ===============================
elif section == "📂 FAQ Categories":
    if not DATASET_CATEGORIES:
        st.warning("No datasets found in the `datasets/` folder.")
    else:
        selected_category = st.selectbox(
            "Select FAQ Category",
            DATASET_CATEGORIES,
        )

        dataset_file = next(
            f
            for f in os.listdir(DATASET_DIR)
            if f.startswith(selected_category)
        )

        dataset_path = os.path.join(DATASET_DIR, dataset_file)

        faqs, retriever, generator = load_category_resources(dataset_path)

        st.success(f"{len(faqs)} FAQs loaded from `{dataset_file}`")

        query = st.text_input(
            "Ask your question",
            placeholder="Type your question here...",
        )

        if query:
            with st.spinner("Searching and generating answer..."):
                retrieved, scores = retriever.search(query, top_k=3)
                answer = generator.generate_answer(query, retrieved)

            st.markdown("### 💡 Answer")
            st.markdown(
                f"""
<div style="background: #f9fafb; padding:18px;
border-left:5px solid #4CAF50;
border-radius:8px; color: #111827;">
{answer}
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown("### 📚 Sources")
            for i, faq in enumerate(retrieved):
                with st.expander(f"Source {i+1} (Score: {scores[i]:.2f})"):
                    st.write(f"**Q:** {faq['question']}")
                    st.write(f"**A:** {faq['answer']}")

# ===============================
# UPLOAD MODE
# ===============================
elif section == "⬆️ Upload FAQs":
    uploaded_file = st.file_uploader(
        "Upload FAQ Dataset (CSV, JSON, TXT)",
        type=["csv", "json", "txt"],
    )

    if uploaded_file:
        faqs = load_faq_from_uploaded_file(uploaded_file)
        retriever = FAQRetriever()
        retriever.build_index(faqs)
        generator = FAQGenerator(groq_api_key)

        st.success(f"{len(faqs)} FAQs loaded.")

        query = st.text_input(
            "Ask your question",
            placeholder="Type your question here...",
        )

        if query:
            with st.spinner("Generating answer..."):
                retrieved, scores = retriever.search(query, top_k=3)
                answer = generator.generate_answer(query, retrieved)

            st.markdown("### 💡 Answer")
            st.markdown(
                f"""
<div style="background:#f9fafb; padding:18px;
border-left:5px solid #4CAF50;
border-radius:8px;">
{answer}
</div>
""",
                unsafe_allow_html=True,
            )

# ===============================
# FOOTER
# ===============================
st.divider()
st.caption("FAQSense • RAG-powered FAQ Assistant • Streamlit Deployment")

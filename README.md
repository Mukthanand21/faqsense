# FAQSense: RAG-powered FAQ Assistant

A domain-agnostic FAQ system using Retrieval-Augmented Generation (RAG) with Groq API for fast, accurate, and explainable answers.

## Features

- **Data Ingestion**: Supports CSV, JSON, and TXT formats for FAQ data.
- **Retrieval**: Semantic similarity search using embeddings and FAISS vector database.
- **Augmentation**: Injects retrieved FAQs into LLM prompts for grounded responses.
- **Generation**: Ultra-fast inference using Groq API.
- **UI**: Streamlit interface for easy upload and querying.

## Architecture

The system follows a strict RAG pipeline:

1. **Retrieval (R)**: Combine Q&A into semantic chunks, generate embeddings, store in FAISS.
2. **Augmentation (A)**: Use retrieved entries as context in prompts with strict instructions.
3. **Generation (G)**: Generate concise answers grounded in provided context.

## Installation

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Get a Groq API key from [Groq Console](https://console.groq.com/).
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Upload your FAQ file (CSV, JSON, or TXT).
4. Ask questions in natural language.

## File Formats

### CSV
Columns: `question`, `answer`

### JSON
List of objects: `[{"question": "...", "answer": "..."}]`

### TXT
Format:
```
Q: Question 1
A: Answer 1

Q: Question 2
A: Answer 2
```

## Demo

Suitable for hackathon demos due to speed and simplicity.
import pandas as pd
import json
import os

# -------- FOR FILE PATHS (DATASET CATEGORIES) --------
def load_faq_from_path(file_path):
    if not os.path.exists(file_path):
        raise ValueError("File does not exist")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
        return df[["question", "answer"]].to_dict("records")

    elif ext == ".json":
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    elif ext == ".txt":
        faqs = []
        with open(file_path, "r") as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            if lines[i].startswith("Q:"):
                q = lines[i][2:].strip()
                a = lines[i + 1][2:].strip()
                faqs.append({"question": q, "answer": a})
                i += 2
            else:
                i += 1
        return faqs

    else:
        raise ValueError("Unsupported format")

# -------- FOR STREAMLIT UPLOADS --------
def load_faq_from_uploaded_file(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(uploaded_file)
        return df[["question", "answer"]].to_dict("records")

    elif ext == ".json":
        return json.load(uploaded_file)

    elif ext == ".txt":
        content = uploaded_file.read().decode("utf-8").splitlines()
        faqs = []
        i = 0
        while i < len(content):
            if content[i].startswith("Q:"):
                q = content[i][2:].strip()
                a = content[i + 1][2:].strip()
                faqs.append({"question": q, "answer": a})
                i += 2
            else:
                i += 1
        return faqs

    else:
        raise ValueError("Unsupported format")

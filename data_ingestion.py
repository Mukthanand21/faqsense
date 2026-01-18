import pandas as pd
import json
import os


def load_faq_data(file_path):
    """
    Load FAQ data from CSV, JSON, or TXT file and normalize to list of dicts with 'question' and 'answer'.
    """
    if not os.path.exists(file_path):
        raise ValueError("File does not exist.")

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".csv":
        df = pd.read_csv(file_path)
        # Assume columns are 'question' and 'answer'
        if "question" not in df.columns or "answer" not in df.columns:
            raise ValueError("CSV must have 'question' and 'answer' columns.")
        faqs = df[["question", "answer"]].to_dict("records")

    elif file_ext == ".json":
        with open(file_path, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            faqs = data
        else:
            raise ValueError(
                "JSON must be a list of objects with 'question' and 'answer'."
            )
        # Validate each has question and answer
        for item in faqs:
            if "question" not in item or "answer" not in item:
                raise ValueError("Each FAQ must have 'question' and 'answer'.")

    elif file_ext == ".txt":
        with open(file_path, "r") as f:
            lines = f.readlines()
        faqs = []
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith("Q:"):
                question = lines[i].strip()[3:].strip()
                i += 1
                if i < len(lines) and lines[i].strip().startswith("A:"):
                    answer = lines[i].strip()[3:].strip()
                    faqs.append({"question": question, "answer": answer})
                else:
                    raise ValueError(
                        "Invalid TXT format: Answer not found after question."
                    )
            i += 1
    else:
        raise ValueError("Unsupported file format. Use CSV, JSON, or TXT.")

    return faqs

import pandas as pd
import json


def load_faq_from_uploaded_file(uploaded_file):
    """
    Load FAQ data from a Streamlit UploadedFile (CSV, JSON, or TXT)
    and normalize to a list of dicts with keys: 'question', 'answer'.
    """

    filename = uploaded_file.name.lower()

    # ===============================
    # CSV SUPPORT
    # ===============================
    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

        # Normalize column names
        df.columns = [c.lower().strip() for c in df.columns]

        if "question" not in df.columns or "answer" not in df.columns:
            raise ValueError("CSV must contain 'question' and 'answer' columns.")

        faqs = df[["question", "answer"]].dropna().to_dict("records")
        return faqs

    # ===============================
    # JSON SUPPORT
    # ===============================
    elif filename.endswith(".json"):
        try:
            data = json.load(uploaded_file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file.")

        if not isinstance(data, list):
            raise ValueError("JSON must be a list of objects.")

        faqs = []
        for item in data:
            if (
                isinstance(item, dict)
                and "question" in item
                and "answer" in item
            ):
                faqs.append(
                    {
                        "question": str(item["question"]).strip(),
                        "answer": str(item["answer"]).strip(),
                    }
                )
            else:
                raise ValueError(
                    "Each JSON object must contain 'question' and 'answer'."
                )

        return faqs

    # ===============================
    # TXT SUPPORT (Q:/A: FORMAT)
    # ===============================
    elif filename.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8").strip()
        lines = text.splitlines()

        faqs = []
        question = None
        answer_lines = []

        for line in lines:
            line = line.strip()

            if line.startswith("Q:"):
                # Save previous FAQ
                if question and answer_lines:
                    faqs.append(
                        {
                            "question": question,
                            "answer": " ".join(answer_lines).strip(),
                        }
                    )
                    answer_lines = []

                question = line[2:].strip()

            elif line.startswith("A:"):
                answer_lines.append(line[2:].strip())

            elif question and line:
                # Multiline answer support
                answer_lines.append(line)

        # Add last FAQ
        if question and answer_lines:
            faqs.append(
                {
                    "question": question,
                    "answer": " ".join(answer_lines).strip(),
                }
            )

        if not faqs:
            raise ValueError("TXT file contains no valid Q:/A: pairs.")

        return faqs

    # ===============================
    # UNSUPPORTED FORMAT
    # ===============================
    else:
        raise ValueError("Unsupported file format. Use CSV, JSON, or TXT.")

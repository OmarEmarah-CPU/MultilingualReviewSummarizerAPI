"""
This file is meant to experiment the entire project. It was at first as .ipynb on google colab but i downloaded it as .py file to be profuction ready.
"""

import pandas as pd
import re

file_name = "reviews.xlsx"

df = pd.read_excel(file_name)

col_name = next(
    (c for c in df.columns if any(k in c.lower() for k in ["review", "comment", "feedback"])),
    df.columns[0]
)
reviews = df[col_name].dropna().astype(str).tolist()
print(f" Using column → {col_name}   ({len(reviews)} rows)")


def clean_text(text):
    """Remove URLs, punctuation and extra spaces; keep Arabic, Latin letters."""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^A-Za-zÀ-ÿء-ي\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


clean_reviews = [clean_text(r) for r in reviews]


keywords = ["service", "price", "quality", "delivery", "support"]

print(" Variables defined: reviews, clean_reviews, clean_text, keywords")
print(f"🔹 {len(clean_reviews)} cleaned reviews ready for translation.")
print(f"🔹 Example review:\n   {clean_reviews[0][:120]} ...")

import torch, pandas as pd
from importlib import reload
import preprocessing, language_utils, summarizer, keyword_semantics


reload(preprocessing); reload(language_utils); reload(summarizer); reload(keyword_semantics)

print("Using CUDA:", torch.cuda.is_available(),
      "| Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")


file_name = "reviews.xlsx"   
df = pd.read_excel(file_name)
col_name = next((c for c in df.columns if any(k in c.lower() for k in ["review", "comment", "feedback"])),
                 df.columns[0])
reviews = df[col_name].dropna().astype(str).tolist()
print(f"Loaded: {file_name}  |  Using column: {col_name}  ({len(reviews)} rows)")


clean_reviews = preprocessing.preprocess_reviews(reviews)


english_reviews = language_utils.detect_and_translate_reviews(clean_reviews)
print("Translation complete. Example:\n", english_reviews[0][:120], "..." if len(english_reviews[0])>120 else "")


summary = summarizer.generate_summary(english_reviews, target_sentences=2)
print("Summary ready!\n")


print(" Running semantic keyword detection…")
keywords = ["service", "price", "quality", "delivery", "support"]  # ✏️ edit to your keywords
keyword_results = keyword_semantics.semantic_keyword_detection(english_reviews, keywords, threshold=0.3)


print(" Summary:\n", summary)
print("\n Keyword Matches:")
for k, v in keyword_results.items():
    print(f"- {k}: {v if v else 'No semantic match found'}")


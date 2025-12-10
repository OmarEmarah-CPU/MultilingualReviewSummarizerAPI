# summarizer.py
from transformers import pipeline
import torch

device = 0 if torch.cuda.is_available() else -1

#Running the transformer on CUDA
summarizer_model = pipeline("summarization", model="t5-small", device=device)

def generate_summary(reviews, target_sentences=2):
    """
    Generate a concise English summary of all reviews.
    Limits output length to roughly `target_sentences` sentences (2 sentences).
    """
    text = " ".join(reviews)
    text = text[:1500]  # keep within T5-small token limit

    max_len = target_sentences * 40
    min_len = target_sentences * 25

    summary = summarizer_model(
        text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
    )[0]["summary_text"]

    # Trim exactly to the required number of sentences
    sentences = summary.strip().split(". ")
    trimmed = ". ".join(sentences[:target_sentences]).strip()
    if not trimmed.endswith("."):
        trimmed += "."

    return trimmed
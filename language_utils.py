
from transformers import pipeline
from langdetect import detect
import torch

device = 0 if torch.cuda.is_available() else -1

#Transformers pre-trained for translation
translator_ar_en = pipeline("translation", model="Helsinki-NLP/opus-mt-ar-en", device=device)
translator_es_en = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en", device=device)

def detect_and_translate_reviews(reviews):
    translated = []
    for review in reviews:
        try:
            lang = detect(review)
        except:
            lang = "unknown"
        if not review.strip():
            continue
        try:
            if lang == "ar":
                result = translator_ar_en(review)
                translated_text = result[0]['translation_text']
            elif lang == "es":
                result = translator_es_en(review)
                translated_text = result[0]['translation_text']
            else:
                translated_text = review  # English or unknown
        except Exception as e:
            print("⚠️ Translation failed for:", review[:60], "→", e)
            translated_text = review
        translated.append(translated_text)
    return translated

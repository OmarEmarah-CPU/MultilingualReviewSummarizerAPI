
from sentence_transformers import SentenceTransformer, util
import torch

device = 0 if torch.cuda.is_available() else -1

# Sentence Transformer for semantic classification
model_st = SentenceTransformer('all-MiniLM-L6-v2').to("cuda")

def semantic_keyword_detection(reviews, keywords, threshold=0.7):
    keyword_results = {k: [] for k in keywords}
    keyword_embeddings = model_st.encode(keywords, convert_to_tensor=True)

    for review in reviews:
        review_embedding = model_st.encode(review, convert_to_tensor=True)
        # Compute cosine similarity between review and all keywords
        similarities = util.cos_sim(review_embedding, keyword_embeddings)[0]

        for i, keyword in enumerate(keywords):
            if similarities[i] >= threshold:
                keyword_results[keyword].append(review)
    return keyword_results

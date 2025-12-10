
import re
import string

def preprocess_reviews(reviews):
    processed_reviews = []
    for review in reviews:
        # Lowercasing
        review = review.lower()
        # Remove punctuation
        review = review.translate(str.maketrans('', '', string.punctuation))
        # Remove numbers
        review = re.sub(r'\d+', '', review)
        # Remove extra whitespaces
        review = re.sub(r'\s+', ' ', review).strip()
        processed_reviews.append(review)
    return processed_reviews

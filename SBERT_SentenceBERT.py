#requirements: pip install sentence-transformers
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # A popular SBERT model

sentences = [
    "A man is playing a guitar.",
    "A person is playing an instrument.",
    "The cat is sleeping on the mat."
]

# Get sentence embeddings
embeddings = model.encode(sentences)

# Compute similarity between first and second sentence
similarity = util.cos_sim(embeddings[0], embeddings[1])
print(f"Similarity: {similarity.item():.4f}")  # High value = similar meaning

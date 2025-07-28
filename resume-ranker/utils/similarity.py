from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# load the SBERT model once
MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)

def get_embedding(text):
    """Returns embedding vector for the given text."""
    return model.encode([text])[0]

def compute_similarity(emb1, emb2):
    """cosine similarity between two embedding vectors."""
    emb1 = np.array(emb1).reshape(1, -1)
    emb2 = np.array(emb2).reshape(1, -1)
    return cosine_similarity(emb1, emb2)[0][0]

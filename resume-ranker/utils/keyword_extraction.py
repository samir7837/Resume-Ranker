from keybert import KeyBERT

# Load model once for efficiency
kw_model = KeyBERT('all-MiniLM-L6-v2')

def extract_keywords(text, num_keywords=10):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1,2),
        stop_words='english',
        top_n=num_keywords
    )
    # Return just the keyword strings
    return [kw[0] for kw in keywords]

def find_missing_keywords(jd_keywords, resume_text):
    resume_lower = resume_text.lower()
    missing = []
    for kw in jd_keywords:
        # Case-insensitive substring match
        if kw.lower() not in resume_lower:
            missing.append(kw)
    return missing

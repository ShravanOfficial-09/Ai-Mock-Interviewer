import spacy
from textblob import TextBlob

# Load SpaCy Model
nlp = spacy.load("en_core_web_sm")

def tokenize_text(text):
    """Splits text into tokens."""
    doc = nlp(text)
    return [token.text for token in doc]

def pos_tagging(text):
    """Returns Part of Speech tagging."""
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

def extract_entities(text):
    """Extracts Named Entities."""
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def analyze_sentence_structure(text):
    """Analyzes sentence dependency parsing."""
    doc = nlp(text)
    return [(token.text, token.dep_, token.head.text) for token in doc]

def analyze_sentiment(text):
    """Returns sentiment polarity (-1 to 1) and subjectivity (0 to 1)."""
    analysis = TextBlob(text)
    return analysis.sentiment  # Polarity (-1 to 1), Subjectivity (0 to 1)

if __name__ == "__main__":
    sample_text = "I have experience working at Google and Amazon."
    print("Tokens:", tokenize_text(sample_text))
    print("POS Tags:", pos_tagging(sample_text))
    print("Named Entities:", extract_entities(sample_text))
    print("Sentence Structure:", analyze_sentence_structure(sample_text))
    print("Sentiment:", analyze_sentiment(sample_text))


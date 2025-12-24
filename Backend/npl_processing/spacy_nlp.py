import spacy

# Load a Pre-trained Model
nlp = spacy.load("en_core_web_sm")

def process_text(text):
    """Process text with spaCy and return tokenization & POS tagging."""
    doc = nlp(text)

    # Tokenization (Breaking Text into Words)
    tokens = [token.text for token in doc]

    # Part of Speech (POS) Tagging
    pos_tags = [(token.text, token.pos_) for token in doc]

    return tokens, pos_tags

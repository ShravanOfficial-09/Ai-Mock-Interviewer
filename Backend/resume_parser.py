import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Example set of known tech skills (can be expanded or made dynamic)
KNOWN_SKILLS = [
    "Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning",
    "TensorFlow", "React", "Node.js", "MongoDB", "AWS", "Docker", "Kubernetes"
]

def extract_skills(text):
    doc = nlp(text)
    extracted_skills = []

    for token in doc:
        if token.text in KNOWN_SKILLS:
            extracted_skills.append(token.text)

    return list(set(extracted_skills))  # Remove duplicates

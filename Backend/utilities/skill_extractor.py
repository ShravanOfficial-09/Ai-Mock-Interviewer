import spacy
from typing import List
import re

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Sample tech skills database — you can expand this
SKILL_KEYWORDS = {
    "Python", "Java", "C++", "JavaScript", "React", "Node.js", "MongoDB",
    "SQL", "HTML", "CSS", "Docker", "Kubernetes", "AWS", "GCP", "Azure",
    "TensorFlow", "PyTorch", "Machine Learning", "Data Science", "FastAPI",
    "Spring Boot", "Git", "REST API", "PostgreSQL", "MySQL", "Linux",
    "Pandas", "NumPy", "OpenCV", "HuggingFace", "Firebase"
}

def clean_text(text: str) -> str:
    # Lowercase and remove non-alphanumeric characters except .
    text = re.sub(r"[^a-zA-Z0-9.\s]", " ", text)
    return text.lower()

def extract_skills(resume_text: str) -> List[str]:
    clean_resume = clean_text(resume_text)
    doc = nlp(clean_resume)
    
    extracted_skills = set()
    
    # Match custom keywords
    for token in doc:
        if token.text in [skill.lower() for skill in SKILL_KEYWORDS]:
            extracted_skills.add(token.text.capitalize())

    # Match multi-word skills from phrases
    for skill in SKILL_KEYWORDS:
        if skill.lower() in clean_resume:
            extracted_skills.add(skill)

    return sorted(extracted_skills)

# Example usage
if __name__ == "__main__":
    sample_resume = """
    I am proficient in Python, React, and MongoDB. 
    Worked on deploying ML models using FastAPI and Docker. 
    Also familiar with AWS, SQL, and basic GCP.
    """
    print(extract_skills(sample_resume))

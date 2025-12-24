import pdfplumber
import spacy
from transformers import pipeline

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# AI Model for Answer Evaluation
answer_evaluator = pipeline("text-classification", model="facebook/bart-large-mnli")

# Extract Text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())

# Generate Questions from Resume
def generate_questions_from_resume(resume_text, difficulty="medium"):
    doc = nlp(resume_text)
    skills = [token.text for token in doc.ents if token.label_ in ["SKILL", "EDUCATION"]]
    
    base_questions = {
        "easy": ["What is {}? Explain in simple terms.".format(skill) for skill in skills],
        "medium": ["How does {} work? Provide examples.".format(skill) for skill in skills],
        "hard": ["Explain advanced concepts related to {}.".format(skill) for skill in skills],
    }
    
    return base_questions[difficulty] if skills else ["Tell me about yourself."]

# AI-based Answer Evaluation
def evaluate_answer(answer):
    result = answer_evaluator(answer)
    return result[0]["label"]

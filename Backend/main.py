import spacy
import os
import pdfplumber
import docx
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from Backend.auth import auth_router
from Backend.npl_processing.nlp_processing import tokenize_text, pos_tagging, extract_entities, analyze_sentiment
from Backend.question_generator import QuestionGenerator

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["ai_mock_interviewer"]
collection = db["interview_responses"]

# FastAPI app setup
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined skill set
SKILLS = [
    "python", "java", "c++", "html", "css", "javascript", "react",
    "node.js", "sql", "mongodb", "machine learning", "deep learning",
    "data analysis", "tensorflow", "keras", "pandas", "numpy", "flask",
    "django", "git", "docker", "linux", "fastapi", "nlp"
]

# Skill extraction function
def extract_skills_from_text(text: str):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())
    return list({token.text for token in doc if token.text in SKILLS})

# Question generator instance
generator = QuestionGenerator()

# Include auth router
app.include_router(auth_router)

# Pydantic model
class InterviewResponse(BaseModel):
    candidate_name: str
    response: str

@app.get("/")
def home():
    return {"message": "AI Mock Interviewer API is running!"}

@app.post("/process_response/")  # Handles response processing
async def process_response(interview: InterviewResponse):
    try:
        tokens = tokenize_text(interview.response)
        pos_tags = pos_tagging(interview.response)
        named_entities = extract_entities(interview.response)
        sentiment = analyze_sentiment(interview.response)

        expected_keywords = ["python", "oop", "teamwork", "deadline", "problem-solving"]
        matched_keywords = [kw for kw in expected_keywords if kw in interview.response.lower()]
        score = round((len(matched_keywords) / len(expected_keywords)) * 100, 2)

        if score >= 80:
            feedback = "Excellent! You covered almost everything."
        elif score >= 60:
            feedback = "Good job! You can still include more technical points."
        elif score >= 40:
            feedback = "Fair — try adding more relevant keywords and examples."
        else:
            feedback = "Needs improvement. Add more technical content."

        processed_data = {
            "tokens": tokens,
            "pos_tags": pos_tags,
            "named_entities": named_entities,
            "sentiment": str(sentiment),
            "score": score,
            "feedback": feedback
        }

        collection.insert_one({
            "candidate_name": interview.candidate_name,
            "response": interview.response,
            "processed_data": processed_data
        })

        return {"message": "Response processed successfully.", "data": processed_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        ext = file.filename.split(".")[-1].lower()
        if ext == "pdf":
            with pdfplumber.open(file.file) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        elif ext == "docx":
            doc = docx.Document(file.file)
            text = "\n".join(para.text for para in doc.paragraphs)
        elif ext == "txt":
            text = (await file.read()).decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

        skills = extract_skills_from_text(text)

        # Use extracted skills to generate a question
        if skills:
            primary_skill = skills[0]  # You can improve this logic later
            question = generator.generate_question(domain=primary_skill, difficulty="medium", context=text)
        else:
            question = "Tell me about your technical background."

        return {"question": question, "skills": skills}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")


@app.get("/generate-question/")  # Generate interview questions
def get_generated_question(domain: str = Query("Python"), difficulty: str = Query("medium"), context: str = Query(None)):
    try:
        question = generator.generate_question(domain, difficulty, context)
        return {"question": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

@app.get("/test-db")  # Test MongoDB connection
def test_db():
    try:
        db["test_collection"].insert_one({"message": "MongoDB is connected!"})
        return {"message": "MongoDB connection successful!"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

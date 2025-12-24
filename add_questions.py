from pymongo import MongoClient

# 1️⃣ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 2️⃣ Select the database and collection
db = client["ai_mock_interview"]
collection = db["questions"]

# 3️⃣ Define a list of questions
questions = [
    {
        "question": "What are Python’s key features?",
        "difficulty": "easy",
        "category": "Python"
    },
    {
        "question": "What is the difference between lists and tuples in Python?",
        "difficulty": "medium",
        "category": "Python"
    },
    {
        "question": "Explain garbage collection in Java.",
        "difficulty": "hard",
        "category": "Java"
    }
]

# 4️⃣ Insert the questions into MongoDB
collection.insert_many(questions)

print("✅ Questions added successfully!")


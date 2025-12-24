from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create (or access) a database
db = client["ai_mock_interview"]

# Create (or access) a collection
questions_collection = db["questions"]

# Insert a sample question
sample_question = {
    "question": "What is the difference between Python lists and tuples?",
    "difficulty": "easy",
    "category": "Python"
}

questions_collection.insert_one(sample_question)

print("Sample question added!")

# Verify
for q in questions_collection.find():
    print(q)

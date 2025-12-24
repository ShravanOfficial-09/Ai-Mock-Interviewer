from pymongo import MongoClient

# 1️⃣ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 2️⃣ Select the database and collection
db = client["ai_mock_interview"]
collection = db["questions"]

# 3️⃣ Retrieve all questions
questions = collection.find()

# 4️⃣ Print questions
for question in questions:
    print(question)


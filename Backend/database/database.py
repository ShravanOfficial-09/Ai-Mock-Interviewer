from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database
db = client["ai_mock_interviewer"]

# Define collections
candidates_collection = db["candidates"]
responses_collection = db["responses"]
feedback_collection = db["feedback"]

print("✅ Connected to MongoDB Successfully!")

import os
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic import BaseModel

# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["ai_mock_interviewer"]
user_collection = db["users"]

# Authentication Router
auth_router = APIRouter()

# Models
class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

# Register Route
@auth_router.post("/register")
async def register_user(user: RegisterUser):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)

    user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })

    return {"message": f"User {user.username} registered successfully"}

# Login Route
@auth_router.post("/login")
async def login_user(user: LoginUser):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful"}


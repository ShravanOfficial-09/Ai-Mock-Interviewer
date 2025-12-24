from bson import ObjectId
from Backend.database.database import candidates_collection

# Function to insert a new candidate
def insert_candidate(candidate_data):
    result = candidates_collection.insert_one(candidate_data)
    return str(result.inserted_id)

# Function to fetch all candidates
def get_all_candidates():
    return list(candidates_collection.find({}, {"_id": 0}))

# Function to get a candidate by ID
def get_candidate_by_id(candidate_id):
    return candidates_collection.find_one({"_id": ObjectId(candidate_id)})

# Function to update a candidate's info
def update_candidate(candidate_id, update_data):
    candidates_collection.update_one(
        {"_id": ObjectId(candidate_id)},
        {"$set": update_data}
    )
    return True

# Function to delete a candidate
def delete_candidate(candidate_id):
    candidates_collection.delete_one({"_id": ObjectId(candidate_id)})
    return True

from pymongo import MongoClient
from datetime import datetime, timezone
from config import Config

class DatabaseManager:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.DB_NAME]
            self.farmers_collection = self.db.farmers
            self.conversations_collection = self.db.conversations
            print(" MongoDB connection successful.")
        except Exception as e:
            print(f" MongoDB connection failed: {e}")
            self.client = None

    def get_farmer(self, phone_number: str):
        """Finds a farmer by their phone number."""
        return self.farmers_collection.find_one({"phone_number": phone_number})

    def create_farmer(self, phone_number: str):
        """Creates a new farmer record and starts onboarding."""
        farmer_data = {
            "phone_number": phone_number,
            "onboarding_completed": False,
            "onboarding_step": "name",
            "name": None,
            "location": None,
            "primary_crop": None,
            "registered_at": datetime.now(timezone.utc)
        }
        self.farmers_collection.insert_one(farmer_data)
        return farmer_data

    def update_farmer(self, phone_number: str, data: dict):
        """Updates a farmer's record."""
        self.farmers_collection.update_one(
            {"phone_number": phone_number},
            {"$set": data}
        )

    def save_conversation(self, phone_number: str, role: str, content: str):
        """Saves a message to the conversation history."""
        message_data = {
            "phone_number": phone_number,
            "role": role,  # 'user' or 'assistant'
            "content": content,
            "timestamp": datetime.now(timezone.utc)
        }
        self.conversations_collection.insert_one(message_data)

    def get_conversation_history(self, phone_number: str, limit: int = 6):
        """Retrieves the most recent messages for a user."""
        history = self.conversations_collection.find(
            {"phone_number": phone_number}
        ).sort("timestamp", -1).limit(limit)
        

        return list(reversed(list(history)))

db_manager = DatabaseManager()
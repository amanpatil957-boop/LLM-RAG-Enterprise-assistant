
import os
from dotenv import load_dotenv
from pymongo import MongoClient

print("Starting MongoDB connection test...")

load_dotenv()

uri = os.getenv("MONGODB_URI")
database_name = os.getenv(
    "MONGODB_DATABASE",
    "enterprise_assistant"
)

if not uri:
    raise ValueError(
        "MONGODB_URI is missing. Check your .env file."
    )

print("Connection string loaded. Connecting to Atlas...")

client = MongoClient(
    uri,
    serverSelectionTimeoutMS=10000
)

try:
    client.admin.command("ping")
    db = client[database_name]

    print("MongoDB Atlas connected successfully!")
    print("Database:", database_name)
    print("Collections:", db.list_collection_names())

except Exception as error:
    print("MongoDB connection failed.")
    print("Error:", error)

finally:
    client.close()

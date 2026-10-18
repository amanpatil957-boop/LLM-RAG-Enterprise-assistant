
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

client = MongoClient(os.getenv("MONGODB_URI"))

try:
    db = client["enterprise_assistant"]
    info = db.command(
        "listCollections",
        filter={"name": "document_chunks"}
    )

    collections = info["cursor"]["firstBatch"]

    if collections:
        details = collections[0]
        print("Collection:", details["name"])
        print("Collection options:", details.get("options", {}))
        print("Collection type:", details.get("type", "not specified"))
    else:
        print("Collection not found!")

finally:
    client.close()

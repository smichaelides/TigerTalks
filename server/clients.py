# clients.py - Mock database client for testing
from typing import Dict, Any, List, Optional
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class MockCollection:
    def __init__(self, name: str):
        self.name = name
        self.data = []
    
    def find_one(self, filter_dict: Dict[str, Any], projection: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Mock find_one operation"""
        # Simple mock implementation
        if not self.data:
            return None
        
        # Find matching document
        for doc in self.data:
            match = True
            for key, value in filter_dict.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                result = doc.copy()
                # Apply projection if specified
                if projection:
                    if "messages" in projection and "$slice" in projection["messages"]:
                        slice_val = projection["messages"]["$slice"]
                        if "messages" in result:
                            if slice_val < 0:
                                result["messages"] = result["messages"][slice_val:]
                            else:
                                result["messages"] = result["messages"][:slice_val]
                return result
        return None
    
    def update_one(self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any], upsert: bool = False) -> None:
        """Mock update_one operation"""
        # Find existing document
        existing_doc = None
        for i, doc in enumerate(self.data):
            match = True
            for key, value in filter_dict.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                existing_doc = i
                break
        
        if existing_doc is not None:
            # Update existing document
            for key, value in update_dict.items():
                if key == "$push":
                    for push_key, push_value in value.items():
                        if push_key not in self.data[existing_doc]:
                            self.data[existing_doc][push_key] = []
                        self.data[existing_doc][push_key].append(push_value)
                elif key == "$set":
                    for set_key, set_value in value.items():
                        self.data[existing_doc][set_key] = set_value
        elif upsert:
            # Create new document
            new_doc = filter_dict.copy()
            for key, value in update_dict.items():
                if key == "$push":
                    for push_key, push_value in value.items():
                        new_doc[push_key] = [push_value]
                elif key == "$set":
                    for set_key, set_value in value.items():
                        new_doc[set_key] = set_value
            self.data.append(new_doc)

class MockDatabase:
    def __init__(self):
        self.collections = {}
    
    def __getitem__(self, collection_name: str) -> MockCollection:
        if collection_name not in self.collections:
            self.collections[collection_name] = MockCollection(collection_name)
        return self.collections[collection_name]

# Create a mock database client
db_client = MockDatabase()

# Create OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY not found in environment variables")
    openai_client = None
else:
    openai_client = OpenAI(api_key=api_key)

# For debugging/testing
def print_database_state():
    """Print the current state of the mock database"""
    print("\nMock Database State:")
    for collection_name, collection in db_client.collections.items():
        print(f"\nCollection: {collection_name}")
        if not collection.data:
            print("  (empty)")
        else:
            for i, doc in enumerate(collection.data):
                print(f"  Document {i+1}: {doc}") 
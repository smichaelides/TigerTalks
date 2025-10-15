#!/usr/bin/env python3
"""
Utility functions for data validation and cleanup.
"""

import logging
from typing import Dict, List, Any, Optional
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

class DataValidator:
    """Utility class for validating and cleaning data."""
    
    def __init__(self):
        self.client = MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
        self.db = self.client[os.environ["DATABASE_NAME"]]
    
    def validate_semester_data(self, semester_data: Dict) -> bool:
        """Validate semester data structure."""
        required_fields = ['code', 'name', 'cal_name', 'reg_name', 'start_date', 'end_date']
        
        for field in required_fields:
            if field not in semester_data or not semester_data[field]:
                logger.warning(f"Missing or empty required field: {field}")
                return False
        
        return True
    
    def validate_course_data(self, course_data: Dict) -> bool:
        """Validate course data structure."""
        required_fields = ['course_id', 'catalog_number', 'title', 'semester', 'department']
        
        for field in required_fields:
            if field not in course_data or not course_data[field]:
                logger.warning(f"Missing or empty required field: {field}")
                return False
        
        return True
    
    def clean_string_field(self, value: Any) -> str:
        """Clean and normalize string fields."""
        if value is None:
            return ""
        return str(value).strip()
    
    def clean_numeric_field(self, value: Any) -> float:
        """Clean and normalize numeric fields."""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def get_database_stats(self) -> Dict[str, int]:
        """Get statistics about the database."""
        try:
            courses_count = self.db.courses.count_documents({})
            semesters_count = self.db.semesters.count_documents({})
            
            return {
                'courses': courses_count,
                'semesters': semesters_count
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {'courses': 0, 'semesters': 0}
    
    def clear_collections(self):
        """Clear all data from collections (use with caution!)."""
        try:
            self.db.courses.delete_many({})
            self.db.semesters.delete_many({})
            logger.info("Cleared all collections")
        except Exception as e:
            logger.error(f"Error clearing collections: {e}")
    
    def find_duplicate_courses(self) -> List[Dict]:
        """Find duplicate courses in the database."""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": {"course_id": "$course_id", "semester": "$semester"},
                        "count": {"$sum": 1},
                        "docs": {"$push": "$_id"}
                    }
                },
                {"$match": {"count": {"$gt": 1}}}
            ]
            
            duplicates = list(self.db.courses.aggregate(pipeline))
            return duplicates
        except Exception as e:
            logger.error(f"Error finding duplicates: {e}")
            return []
    
    def remove_duplicate_courses(self):
        """Remove duplicate courses, keeping the first occurrence."""
        try:
            duplicates = self.find_duplicate_courses()
            
            for duplicate in duplicates:
                # Keep the first document, remove the rest
                docs_to_remove = duplicate['docs'][1:]
                for doc_id in docs_to_remove:
                    self.db.courses.delete_one({"_id": doc_id})
            
            logger.info(f"Removed {len(duplicates)} duplicate course groups")
        except Exception as e:
            logger.error(f"Error removing duplicates: {e}")
    
    def close(self):
        """Close database connection."""
        self.client.close()

def main():
    """Main function for data utilities."""
    validator = DataValidator()
    
    print("Database Statistics:")
    stats = validator.get_database_stats()
    print(f"  Courses: {stats['courses']}")
    print(f"  Semesters: {stats['semesters']}")
    
    print("\nChecking for duplicate courses...")
    duplicates = validator.find_duplicate_courses()
    if duplicates:
        print(f"Found {len(duplicates)} duplicate course groups")
        print("Removing duplicates...")
        validator.remove_duplicate_courses()
    else:
        print("No duplicates found")
    
    validator.close()

if __name__ == "__main__":
    main()

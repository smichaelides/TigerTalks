#!/usr/bin/env python3
"""
Test script to verify data population functionality.
"""

import sys
import os
from pathlib import Path

# Add the server directory to the Python path
server_dir = Path(__file__).parent.parent
sys.path.insert(0, str(server_dir))

# Change to the server directory
os.chdir(server_dir)

from data.populate_models import DataPopulator
from data.data_utils import DataValidator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_data_loading():
    """Test loading JSON data files."""
    print("Testing data loading...")
    
    populator = DataPopulator()
    
    # Test loading coursedetails.json
    coursedetails_data = populator.load_json_data('data/coursedetails.json')
    if coursedetails_data:
        print("✓ coursedetails.json loaded successfully")
    else:
        print("✗ Failed to load coursedetails.json")
        return False
    
    # Test loading pdf.json
    pdf_data = populator.load_json_data('data/pdf.json')
    if pdf_data:
        print("✓ pdf.json loaded successfully")
    else:
        print("✗ Failed to load pdf.json")
        return False
    
    # Test loading departmentals.json
    departmentals_data = populator.load_json_data('data/departmentals.json')
    if departmentals_data:
        print("✓ departmentals.json loaded successfully")
    else:
        print("✗ Failed to load departmentals.json")
        return False
    
    populator.client.close()
    return True

def test_semester_parsing():
    """Test semester data parsing."""
    print("\nTesting semester parsing...")
    
    populator = DataPopulator()
    coursedetails_data = populator.load_json_data('data/coursedetails.json')
    
    if coursedetails_data:
        semester = populator.parse_semester_data(coursedetails_data)
        if semester:
            print(f"✓ Semester parsed: {semester.code} - {semester.name}")
            return True
        else:
            print("✗ Failed to parse semester data")
            return False
    else:
        print("✗ No coursedetails data to parse")
        return False

def test_course_parsing():
    """Test course data parsing."""
    print("\nTesting course parsing...")
    
    populator = DataPopulator()
    coursedetails_data = populator.load_json_data('data/coursedetails.json')
    
    if coursedetails_data and 'term' in coursedetails_data:
        term_data = coursedetails_data['term'][0]
        semester_code = term_data.get('code', '')
        
        # Find first course to test
        first_course = None
        for subject in term_data.get('subjects', []):
            if subject.get('courses'):
                first_course = subject['courses'][0]
                break
        
        if first_course:
            course = populator.parse_course_data(first_course, semester_code)
            if course:
                print(f"✓ Course parsed: {course.course_id} - {course.title}")
                return True
            else:
                print("✗ Failed to parse course data")
                return False
        else:
            print("✗ No courses found in data")
            return False
    else:
        print("✗ No coursedetails data to parse")
        return False

def test_database_connection():
    """Test database connection."""
    print("\nTesting database connection...")
    
    try:
        validator = DataValidator()
        stats = validator.get_database_stats()
        print(f"✓ Database connected. Current stats: {stats}")
        validator.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def main():
    """Run all tests."""
    print("TigerTalks Data Population Test Suite")
    print("=" * 50)
    
    tests = [
        test_data_loading,
        test_semester_parsing,
        test_course_parsing,
        test_database_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Data population should work correctly.")
        return True
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

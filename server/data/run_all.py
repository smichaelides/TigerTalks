#!/usr/bin/env python3
"""
Comprehensive script to run all data population tasks.
This script orchestrates the entire data population process.
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

def run_complete_population():
    """Run the complete data population process."""
    print("TigerTalks Complete Data Population Process")
    print("=" * 60)
    
    try:
        # Step 1: Test data loading and parsing
        print("\n1. Testing data loading and parsing...")
        from data.test_population import main as test_main
        if not test_main():
            print("❌ Tests failed. Please fix issues before proceeding.")
            return False
        
        # Step 2: Clear existing data (optional)
        print("\n2. Checking for existing data...")
        validator = DataValidator()
        stats = validator.get_database_stats()
        print(f"   Current database stats: {stats}")
        
        if stats['courses'] > 0 or stats['semesters'] > 0:
            response = input("   Found existing data. Clear it? (y/N): ").strip().lower()
            if response == 'y':
                print("   Clearing existing data...")
                validator.clear_collections()
            else:
                print("   Keeping existing data (may create duplicates)")
        
        validator.close()
        
        # Step 3: Run data population
        print("\n3. Running data population...")
        populator = DataPopulator()
        populator.run()
        
        # Step 4: Validate results
        print("\n4. Validating results...")
        validator = DataValidator()
        final_stats = validator.get_database_stats()
        print(f"   Final database stats: {final_stats}")
        
        # Check for duplicates
        duplicates = validator.find_duplicate_courses()
        if duplicates:
            print(f"   Found {len(duplicates)} duplicate course groups")
            response = input("   Remove duplicates? (Y/n): ").strip().lower()
            if response != 'n':
                validator.remove_duplicate_courses()
                print("   Duplicates removed")
        else:
            print("   No duplicates found")
        
        validator.close()
        
        print("\n✅ Data population completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error in complete population process: {e}")
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main function."""
    print("This script will:")
    print("1. Test data loading and parsing")
    print("2. Check for existing data")
    print("3. Populate the database with course and semester data")
    print("4. Validate and clean up the results")
    print("\nMake sure your .env file is configured with MongoDB connection details.")
    
    response = input("\nProceed? (Y/n): ").strip().lower()
    if response == 'n':
        print("Cancelled by user.")
        return
    
    success = run_complete_population()
    
    if success:
        print("\n🎉 All done! Your TigerTalks database is now populated with course data.")
    else:
        print("\n💥 Something went wrong. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

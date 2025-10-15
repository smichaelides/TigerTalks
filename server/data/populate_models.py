#!/usr/bin/env python3
"""
Script to parse JSON data files and populate Course and Semester models.
This script processes three JSON files:
1. coursedetails.json - Main course data with detailed information
2. pdf.json - Course data with PDF requirements
3. departmentals.json - Department and subject information
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Import our models
from api.models.courses import Course, PDF, GradingComponent, Detail, Instructor, Crosslisting, ClassSection, Meeting, Building, Schedule
from api.models.semester import Semester

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataPopulator:
    def __init__(self):
        """Initialize the data populator with database connection."""
        self.client = MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
        self.db = self.client[os.environ["DATABASE_NAME"]]
        self.courses_collection = self.db.courses
        self.semesters_collection = self.db.semesters
        
    def load_json_data(self, file_path: str) -> Any:
        """Load JSON data from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return None
    
    def parse_semester_data(self, coursedetails_data: Dict) -> Optional[Semester]:
        """Parse semester information from coursedetails.json."""
        try:
            if 'term' in coursedetails_data and len(coursedetails_data['term']) > 0:
                term_data = coursedetails_data['term'][0]
                
                semester = Semester(
                    _id=ObjectId(),
                    code=term_data.get('code', ''),
                    name=term_data.get('name', ''),
                    cal_name=term_data.get('cal_name', ''),
                    reg_name=term_data.get('reg_name', ''),
                    start_date=term_data.get('start_date', ''),
                    end_date=term_data.get('end_date', '')
                )
                return semester
        except Exception as e:
            logger.error(f"Error parsing semester data: {e}")
        return None
    
    def parse_course_data(self, course_data: Dict, semester_code: str) -> Optional[Course]:
        """Parse individual course data from JSON."""
        try:
            # Parse PDF information
            pdf_data = course_data.get('pdf', {})
            pdf = PDF(
                required=pdf_data.get('required', False),
                permitted=pdf_data.get('permitted', False)
            )
            
            # Parse grading components
            grading_components = []
            for grade_data in course_data.get('grading', []):
                grading_components.append(GradingComponent(
                    component=grade_data.get('component', ''),
                    weight=grade_data.get('weight', 0.0)
                ))
            
            # Parse detail information
            detail_data = course_data.get('detail', {})
            detail = None
            if detail_data:
                detail = Detail(
                    start_date=detail_data.get('start_date', ''),
                    end_date=detail_data.get('end_date', ''),
                    track=detail_data.get('track', ''),
                    description=detail_data.get('description', ''),
                    seat_reservations=detail_data.get('seat_reservations', '')
                )
            
            # Parse instructors
            instructors = []
            for instructor_data in course_data.get('instructors', []):
                instructors.append(Instructor(
                    emplid=instructor_data.get('emplid', ''),
                    first_name=instructor_data.get('first_name', ''),
                    last_name=instructor_data.get('last_name', ''),
                    full_name=instructor_data.get('full_name', '')
                ))
            
            # Parse crosslistings
            crosslistings = []
            for crosslist_data in course_data.get('crosslistings', []):
                crosslistings.append(Crosslisting(
                    subject=crosslist_data.get('subject', ''),
                    catalog_number=crosslist_data.get('catalog_number', '')
                ))
            
            # Parse class sections
            classes = []
            for class_data in course_data.get('classes', []):
                # Parse schedule information
                schedule_data = class_data.get('schedule', {})
                meetings = []
                
                for meeting_data in schedule_data.get('meetings', []):
                    building_data = meeting_data.get('building', {})
                    building = Building(
                        location_code=building_data.get('location_code', ''),
                        name=building_data.get('name', '')
                    )
                    
                    meeting = Meeting(
                        meeting_number=meeting_data.get('meeting_number', ''),
                        start_time=meeting_data.get('start_time', ''),
                        end_time=meeting_data.get('end_time', ''),
                        room=meeting_data.get('room', ''),
                        days=meeting_data.get('days', []),
                        building=building
                    )
                    meetings.append(meeting)
                
                schedule = Schedule(
                    start_date=schedule_data.get('start_date', ''),
                    end_date=schedule_data.get('end_date', ''),
                    meetings=meetings
                )
                
                class_section = ClassSection(
                    class_number=class_data.get('class_number', ''),
                    section=class_data.get('section', ''),
                    status=class_data.get('status', ''),
                    pu_calc_status=class_data.get('pu_calc_status', ''),
                    seat_status=class_data.get('seat_status', ''),
                    type_name=class_data.get('type_name', ''),
                    capacity=class_data.get('capacity', ''),
                    enrollment=class_data.get('enrollment', ''),
                    schedule=schedule
                )
                classes.append(class_section)
            
            # Create Course object
            course = Course(
                guid=course_data.get('guid'),
                course_id=course_data.get('course_id', ''),
                catalog_number=course_data.get('catalog_number', ''),
                title=course_data.get('title', ''),
                semester=int(semester_code) if semester_code.isdigit() else 0,
                department=course_data.get('department', ''),
                description=course_data.get('description'),
                detail=detail,
                pdf=pdf,
                audit=course_data.get('audit', False),
                grading=grading_components,
                assignments=course_data.get('assignments', ''),
                reserved_seats=course_data.get('reserved_seats', []),
                readings=course_data.get('readings', []),
                prerequisites=course_data.get('prerequisites', ''),
                other_information=course_data.get('other_information', ''),
                other_requirements=course_data.get('other_requirements', ''),
                website=course_data.get('website', ''),
                distribution=course_data.get('distribution', ''),
                open=course_data.get('open', True),
                new=course_data.get('new', False),
                instructors=instructors if instructors else None,
                crosslistings=crosslistings if crosslistings else None,
                classes=classes if classes else None
            )
            
            return course
            
        except Exception as e:
            logger.error(f"Error parsing course data: {e}")
            return None
    
    def populate_semester(self, semester: Semester) -> bool:
        """Insert semester data into database."""
        try:
            # Check if semester already exists
            existing = self.semesters_collection.find_one({"code": semester.code})
            if existing:
                logger.info(f"Semester {semester.code} already exists, skipping...")
                return True
            
            # Convert to dict for MongoDB insertion
            semester_dict = semester.model_dump()
            semester_dict['_id'] = semester._id
            
            result = self.semesters_collection.insert_one(semester_dict)
            logger.info(f"Inserted semester {semester.code} with ID: {result.inserted_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting semester: {e}")
            return False
    
    def populate_courses(self, courses: List[Course]) -> int:
        """Insert course data into database."""
        inserted_count = 0
        skipped_count = 0
        
        for course in courses:
            try:
                # Check if course already exists
                existing = self.courses_collection.find_one({
                    "course_id": course.course_id,
                    "semester": course.semester
                })
                
                if existing:
                    logger.debug(f"Course {course.course_id} already exists, skipping...")
                    skipped_count += 1
                    continue
                
                # Convert to dict for MongoDB insertion
                course_dict = course.model_dump()
                
                result = self.courses_collection.insert_one(course_dict)
                logger.debug(f"Inserted course {course.course_id} with ID: {result.inserted_id}")
                inserted_count += 1
                
            except Exception as e:
                logger.error(f"Error inserting course {course.course_id}: {e}")
        
        logger.info(f"Inserted {inserted_count} courses, skipped {skipped_count} existing courses")
        return inserted_count
    
    def process_coursedetails_data(self, coursedetails_data: Dict) -> tuple[Optional[Semester], List[Course]]:
        """Process coursedetails.json data."""
        semester = self.parse_semester_data(coursedetails_data)
        courses = []
        
        if 'term' in coursedetails_data and len(coursedetails_data['term']) > 0:
            term_data = coursedetails_data['term'][0]
            semester_code = term_data.get('code', '')
            
            # Process courses from each subject
            for subject in term_data.get('subjects', []):
                for course_data in subject.get('courses', []):
                    course = self.parse_course_data(course_data, semester_code)
                    if course:
                        courses.append(course)
        
        return semester, courses
    
    def process_pdf_data(self, pdf_data: List) -> List[Course]:
        """Process pdf.json data to supplement course information."""
        courses = []
        
        for course_data in pdf_data:
            print(course_data)
            try:
                # Extract semester from the first course if available
                semester_code = str(course_data.get('semester', ''))
                course = self.parse_course_data(course_data, semester_code)
                if course:
                    courses.append(course)
            except Exception as e:
                logger.error(f"Error processing PDF course data: {e}")
        
        return courses
    
    def merge_course_data(self, coursedetails_courses: List[Course], pdf_courses: List[Course]) -> List[Course]:
        """Merge course data from different sources, prioritizing coursedetails data."""
        course_dict = {}
        
        # Add coursedetails courses first (higher priority)
        for course in coursedetails_courses:
            key = f"{course.course_id}_{course.semester}"
            course_dict[key] = course
        
        # Add PDF courses if not already present
        for course in pdf_courses:
            key = f"{course.course_id}_{course.semester}"
            if key not in course_dict:
                course_dict[key] = course
        
        return list(course_dict.values())
    
    def run(self):
        """Main execution method."""
        logger.info("Starting data population process...")
        
        # Load JSON data files
        logger.info("Loading JSON data files...")
        coursedetails_data = self.load_json_data('data/coursedetails.json')
        pdf_data = self.load_json_data('data/pdf.json')
        departmentals_data = self.load_json_data('data/departmentals.json')
        
        if not coursedetails_data:
            logger.error("Failed to load coursedetails.json")
            return
        
        # Process coursedetails data
        logger.info("Processing coursedetails data...")
        semester, coursedetails_courses = self.process_coursedetails_data(coursedetails_data)
        
        # Process PDF data
        logger.info("Processing PDF data...")
        pdf_courses = self.process_pdf_data(pdf_data) if pdf_data else []
        
        # Merge course data
        logger.info("Merging course data...")
        all_courses = self.merge_course_data(coursedetails_courses, pdf_courses)
        
        # Populate database
        logger.info("Populating database...")
        
        # Insert semester
        if semester:
            self.populate_semester(semester)
        
        # Insert courses
        if all_courses:
            self.populate_courses(all_courses)
        
        logger.info(f"Data population completed. Processed {len(all_courses)} courses.")
        
        # Close database connection
        self.client.close()

def main():
    """Main function to run the data population script."""
    try:
        populator = DataPopulator()
        populator.run()
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()

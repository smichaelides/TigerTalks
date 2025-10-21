#!/usr/bin/env python3
"""
Course Web Data Import Script
Scrapes course data from Princeton's StudentApp API and Registrar API
Similar to the JavaScript version but adapted for Python/Flask/MongoDB
"""

import subprocess
import json
import sys
import os
from typing import Dict, Any, Optional
import logging
from bs4 import BeautifulSoup
import requests


# Add the server directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Assignment mapping for grading components
ASSIGNMENT_MAPPING = {
    'grading_mid_exam': 'Mid term exam',
    'grading_paper_mid_exam': 'Paper in lieu of mid term',
    'grading_final_exam': 'Final exam',
    'grading_paper_final_exam': 'Paper in lieu of final',
    'grading_other_exam': 'Other exam',
    'grading_home_mid_exam': 'Take home mid term exam',
    'grading_design_projects': 'Design project',
    'grading_home_final_exam': 'Take home final exam',
    'grading_prog_assign': 'Programming assignments',
    'grading_quizzes': 'Quizzes',
    'grading_lab_reports': 'Lab reports',
    'grading_papers': 'Papers',
    'grading_oral_pres': 'Oral presentation(s)',
    'grading_term_papers': 'Term paper(s)',
    'grading_precept_part': 'Class/precept participation',
    'grading_prob_sets': 'Problem set(s)',
    'grading_other': 'Other (see instructor)'
}

ASSIGNMENT_PROPERTY_NAMES = list(ASSIGNMENT_MAPPING.keys())

# Global variables
registrar_frontend_api_token = None
courses_pending_processing = 0
db = None


def load_courses_from_studentapp(query: str = "") -> Dict[str, Any]:
    """Call the studentapp.py script to get basic course data"""
    logger.info("Preparing to make request to StudentApp API for course listings data")
    
    args = ["python", "data/studentapp.py", "importBasicCourseDetails"]
    if query:
        args.append(query)
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if result.returncode != 0:
            logger.error(f"StudentApp script failed: {result.stderr}")
            return {}
        
        return json.loads(result.stdout)
    except Exception as e:
        logger.error(f"Error calling StudentApp script: {e}")
        return {}


def import_data_from_studentapp(data: Dict[str, Any]) -> None:
    """Process the data received from StudentApp API"""
    logger.info("Processing data received from StudentApp API")
    
    if not data or 'term' not in data:
        logger.error("No term data found in StudentApp response")
        return
    
    # Convert term code to integer
    data['term'][0]['code'] = int(data['term'][0]['code'])

    terms = []
    
    for term in data['term']:
        terms.append(import_term(term))

    return terms


def import_term(term: Dict[str, Any]) -> None:
    """Import a semester term into the database"""
    logger.info(f"Processing the {term['cal_name']} semester")
    
    # Create/update semester in database
    semester_data = {
        "code": term['code'],
        "name": term['cal_name'],
        "start_date": term.get('start_date'),
        "end_date": term.get('end_date')
    }
    
    try:
        # # Upsert semester
        # db.semesters.update_one(
        #     {"code": term['code']},
        #     {"$set": semester_data},
        #     upsert=True
        # )
        logger.info(f"Successfully created/updated semester {term['cal_name']}")
        
        subjects = []

        # Process each subject within this semester
        for subject in term.get('subjects', []):
            subject = import_subject(term, subject)
            subjects.append(subject)

        return subject
    except Exception as e:
        logger.error(f"Failed to create/update semester {term['cal_name']}: {e}")


def decode_escaped_characters(html: str) -> str:
    """Decode escaped HTML characters"""
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def import_subject(semester: Dict[str, Any], subject: Dict[str, Any]) -> None:
    """Import courses from a subject/department"""
    logger.debug(f"Processing subject {subject['code']} in semester {semester['cal_name']}")


    courses = []
    
    for course_data in subject.get('courses', []):
        # Skip courses with invalid catalog numbers
        if not course_data.get('catalog_number') or len(course_data['catalog_number']) < 2:
            continue
        
        # Decode HTML characters in title and description
        if course_data.get('title'):
            course_data['title'] = decode_escaped_characters(course_data['title'])
        
        if course_data.get('detail', {}).get('description'):
            course_data['detail']['description'] = decode_escaped_characters(course_data['detail']['description'])
        
        # Get detailed course information from registrar API
        courses.append(get_course_details(semester, subject['code'], course_data))

    return courses


def get_course_details(semester: Dict[str, Any], subject_code: str, course_data: Dict[str, Any]) -> None:
    """Get detailed course information from registrar API"""
    global courses_pending_processing
    
    if not registrar_frontend_api_token:
        logger.error("No registrar frontend API token available")
        return
    
    url = f"https://api.princeton.edu/registrar/course-offerings/course-details?term={semester['code']}&course_id={course_data['course_id']}"
    headers = {
        'Pragma': 'no-cache',
        'Accept': 'application/json',
        'Authorization': f'Bearer {registrar_frontend_api_token}',
        'User-Agent': 'Princeton Courses (https://www.princetoncourses.com)'
    }
    
    courses_pending_processing += 1
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            logger.warning(f"Skipping {course_data['course_id']}: registrar responded with status {response.status_code}")
            courses_pending_processing -= 1
            return
        
        logger.info(f"Got results for {course_data['course_id']}")
        
        try:
            parsed = response.json()
        except json.JSONDecodeError as e:
            logger.warning(f"Skipping {course_data['course_id']}: failed to parse registrar JSON ({e})")
            courses_pending_processing -= 1
            return
        
        details_root = parsed.get('course_details')
        details_arr = details_root.get('course_detail') if details_root else None
        
        if not details_arr or not isinstance(details_arr, list) or len(details_arr) == 0:
            logger.warning(f"Skipping {course_data['course_id']}: no course_detail found in registrar response")
            courses_pending_processing -= 1
            return
        
        frontend_api_course_details = details_arr[0]
        
        # Process grading basis
        process_grading_basis(course_data, frontend_api_course_details)
        
        # Process grading components
        process_grading_components(course_data, frontend_api_course_details)
        
        # Process assignments
        process_assignments(course_data, frontend_api_course_details)
        
        # Process reserved seats
        process_reserved_seats(course_data, frontend_api_course_details)
        
        # Process reading list
        process_reading_list(course_data, frontend_api_course_details)
        
        # Process other course information
        process_other_information(course_data, frontend_api_course_details)
        
        # Create course in database
        course = create_course(semester, subject_code, course_data)
        
        return course
    except Exception as e:
        logger.error(f"Error processing course {course_data['course_id']}: {e}")
        courses_pending_processing -= 1


def process_grading_basis(course_data: Dict[str, Any], details: Dict[str, Any]) -> None:
    """Process grading basis (P/D/F, audit, etc.)"""
    grading_basis = details.get('grading_basis', '')
    
    if grading_basis == 'FUL':  # Graded A-F, P/D/F, Audit
        course_data['pdf'] = {'required': False, 'permitted': True}
        course_data['audit'] = True
    elif grading_basis == 'NAU':  # No Audit
        course_data['pdf'] = {'required': False, 'permitted': True}
        course_data['audit'] = False
    elif grading_basis == 'GRD':  # na, npdf
        course_data['pdf'] = {'required': False, 'permitted': False}
        course_data['audit'] = False
    elif grading_basis == 'NPD':  # No Pass/D/Fail
        course_data['pdf'] = {'required': False, 'permitted': False}
        course_data['audit'] = True
    elif grading_basis == 'PDF':  # P/D/F Only
        course_data['pdf'] = {'required': True, 'permitted': True}
        course_data['audit'] = True
    else:
        course_data['pdf'] = {'required': False, 'permitted': True}
        course_data['audit'] = True




def process_grading_components(course_data: Dict[str, Any], details: Dict[str, Any]) -> None:
    """Process grading components and weights"""
    grading = []
    
    for key, value in details.items():
        if key in ASSIGNMENT_PROPERTY_NAMES and value != '0':
            grading.append({
                'component': ASSIGNMENT_MAPPING[key],
                'weight': float(value)
            })
    
    # Sort by weight (descending)
    grading.sort(key=lambda x: x['weight'], reverse=True)
    course_data['grading'] = grading


def process_assignments(course_data: Dict[str, Any], details: Dict[str, Any]) -> None:
    """Process assignment descriptions"""
    assignment_desc = details.get('reading_writing_assignment')
    if assignment_desc and assignment_desc.strip():
        course_data['assignments'] = assignment_desc.strip()


def process_reserved_seats(course_data: Dict[str, Any], details: Dict[str, Any]) -> None:
    """Process reserved seats information"""
    seat_reservations = details.get('seat_reservations', {})
    if seat_reservations.get('seat_reservation'):
        course_data['reserved_seats'] = [
            f"{reservation['description']} {reservation['enrl_cap']}"
            for reservation in seat_reservations['seat_reservation']
        ]


def process_reading_list(course_data: Dict[str, Any], details: Dict[str, Any]) -> None:
    """Process reading list"""
    reading_list = []
    
    for i in range(1, 7):  # Check reading_list_title_1 through reading_list_title_6
        title = details.get(f'reading_list_title_{i}')
        if title and title.strip():
            reading = {'title': title.strip()}
            
            author = details.get(f'reading_list_author_{i}')
            if author and author.strip():
                reading['author'] = author.strip()
            
            reading_list.append(reading)
    
    if reading_list:
        course_data['reading_list'] = reading_list


def process_other_information(course_data: Dict[str, Any], details: Dict[str, Any]) -> None:
    """Process other course information"""
    course_data['prerequisites'] = details.get('other_restrictions')
    course_data['other_information'] = details.get('other_information')
    course_data['other_requirements'] = details.get('other_requirements')
    course_data['website'] = details.get('web_address')
    course_data['distribution_area'] = details.get('distribution_area_short')


def create_course(semester: Dict[str, Any], subject_code: str, course_data: Dict[str, Any]) -> None:
    """Create course in database"""
    # Prepare course document
    course_doc = {
        'course_id': course_data['course_id'],
        'catalog_number': course_data['catalog_number'],
        'title': course_data['title'],
        'semester': semester['code'],
        'department': subject_code,
        'description': course_data.get('detail', {}).get('description'),
        'pdf': course_data.get('pdf', {'permitted': True, 'required': False}),
        'audit': course_data.get('audit', True),
        'grading': course_data.get('grading', []),
        'assignments': course_data.get('assignments'),
        'reserved_seats': course_data.get('reserved_seats', []),
        'readings': course_data.get('reading_list', []),
        'prerequisites': course_data.get('prerequisites'),
        'other_information': course_data.get('other_information'),
        'other_requirements': course_data.get('other_requirements'),
        'website': course_data.get('website'),
        'distribution': course_data.get('distribution_area'),
        'open': True,
        'new': False
    }

    return course_doc

def get_registrar_frontend_api_token() -> Optional[str]:
    """Get the registrar frontend API token"""
    # Check if token is provided in environment
    token = os.environ.get('REGISTRAR_FE_API_TOKEN')
    if token and token.strip():
        return token.strip()
    
    # Try to scrape token from registrar website
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get('https://registrar.princeton.edu/course-offerings', headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        logger.info("Successfully fetched registrar page")
        
        # Look for drupal-settings-json element
        drupal_settings = soup.find(attrs={'data-drupal-selector': 'drupal-settings-json'})
        if drupal_settings and drupal_settings.text:
            logger.info("Found drupal-settings-json element")
            try:
                data = json.loads(drupal_settings.text)
                if data and data.get('ps_registrar', {}).get('apiToken'):
                    token = data['ps_registrar']['apiToken']
                    logger.info(f"Found API token in drupal settings: {token[:20]}...")
                    return token
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse drupal settings JSON: {e}")
        
        # Fallback: regex search through all scripts
        logger.info("Searching for API token in script tags")
        for script in soup.find_all('script'):
            if script.string:
                import re
                match = re.search(r'"apiToken"\s*:\s*"([^"]+)"', script.string)
                if match:
                    token = match.group(1)
                    logger.info(f"Found API token in script: {token[:20]}...")
                    return token
        
        logger.error("Could not locate registrar front-end API token")
        return None
        
    except Exception as e:
        logger.error(f"Error getting registrar frontend API token: {e}")
        return None


def main():
    """Main function"""
    global registrar_frontend_api_token, db


    
    logger.info("Starting script to update database with latest course listings information")
    
    # Get query string from command line args
    query_string = sys.argv[2] if len(sys.argv) > 2 else ""
    
    # Get registrar frontend API token
    logger.info("Acquiring API token for the registrar's website front-end API")
    registrar_frontend_api_token = get_registrar_frontend_api_token()
    
    if not registrar_frontend_api_token:
        logger.error("Failed to get registrar frontend API token")
        sys.exit(1)
    
    logger.info("Got registrar frontend API token")
    
    # Load courses from StudentApp API
    data = load_courses_from_studentapp(query_string)
    if not data:
        logger.error("No data received from StudentApp API")
        sys.exit(1)
    
    # Process the data
    terms = import_data_from_studentapp(data)
    print(terms)

if __name__ == "__main__":
    main()

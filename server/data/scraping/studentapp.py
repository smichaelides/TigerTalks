# ----------------------------------------------------------------------
# studentapp.py
# Contains StudentApp, a class used to communicate with the StudentApp API
# from the Princeton OIT.
# Handles API communication with StudentApp API & manages authentication
# tokens and API endpoints.
# Credit: vr2amesh https://github.com/vr2amesh/COS333-API-Code-Examples
# ----------------------------------------------------------------------

import requests 
import json
from dotenv import load_dotenv
import os
import base64
import sys


load_dotenv()

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]

class StudentApp:

    def __init__(self):
        self.configs = Configs()
        # Single session reused for all requests; helps with connection pooling
        self._session = requests.Session()

    def get_courses(self, args):
        return self._getJSON(self.configs.COURSE_COURSES, args)

    def get_all_dept_codes_csv(self):
        data = self._getJSON(self.configs.COURSE_COURSES, 'subject=list')
        return ','.join([e['code'] for e in data['term'][0]['subjects']])

    def get_all_dept_codes_json(self):
        return self._getJSON(self.configs.COURSE_COURSES, 'subject=list')

    def get_terms(self):
        return self._getJSON(self.configs.COURSE_TERMS, 'fmt=json')

    def _getJSON(self, endpoint, args):
        req = requests.get(
            self.configs.BASE_URL + endpoint + '?fmt=json&' + args,
            headers={
                "Authorization": "Bearer " + self.configs.ACCESS_TOKEN
            },
        )
        text = req.text

        # Check to see if the response failed due to invalid credentials
        text = self._updateConfigs(text, endpoint, args)

        return json.loads(text)

    def _updateConfigs(self, text, endpoint, args):
        if text.startswith("<ams:fault"):
            self.configs._refreshToken(grant_type="client_credentials")

            # Redo the request with the new access token
            req = self._session.get(
                self.configs.BASE_URL + endpoint + '?fmt=json&' + args,
                headers={
                    "Authorization": "Bearer " + self.configs.ACCESS_TOKEN
                },
            )
            text = req.text

        return text

class Configs:
    def __init__(self):
        self.consumer_key = CONSUMER_KEY
        self.consumer_secret = CONSUMER_SECRET
        self.BASE_URL = 'https://api.princeton.edu:443/student-app/1.0.3'
        self.COURSE_COURSES = '/courses/courses'
        self.COURSE_TERMS = '/courses/terms'
        self.REFRESH_TOKEN_URL = 'https://api.princeton.edu:443/token'
        self._refreshToken(grant_type='client_credentials')

    def _refreshToken(self, **args):
        req = requests.post(
            self.REFRESH_TOKEN_URL,
            data=args,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes(self.consumer_key + ':' + self.consumer_secret, 'utf-8')).decode('utf-8')
            },
        )
        text = req.text
        response = json.loads(text)
        self.ACCESS_TOKEN = response['access_token']

def main():
    """
    Run like:

    python server/coursedata/studentapp.py importBasicCourseDetails
    python server/coursedata/studentapp.py importBasicCourseDetails "term=1222"
    python server/coursedata/studentapp.py importBasicCourseDetails "subject=COS,EEB&term=1222"
    python server/coursedata/studentapp.py importDepartmentals
    """
    studentapp = StudentApp()
    argv = sys.argv
    if len(argv) < 2:
        print(json.dumps({"error": "Missing command"}))
        sys.stdout.flush()
        return

    if argv[1] == 'importBasicCourseDetails':
        all_codes = studentapp.get_all_dept_codes_csv()
        most_recent_term = studentapp.get_terms()["term"][0]["code"]
        # Build args: if a query was provided but without a subject, expand to all department codes.
        if len(argv) > 2:
            raw = argv[2]
            # If subject is omitted or explicitly 'all', replace with full subject list
            if 'subject=' not in raw:
                args = f'subject={all_codes}&{raw}'
            else:
                args = raw.replace('subject=all', f'subject={all_codes}')
        else:
            args = f'subject={all_codes}&term={most_recent_term}'
        print(json.dumps(studentapp.get_courses(args)))
    elif argv[1] == 'importDepartmentals':
        print(json.dumps(studentapp.get_all_dept_codes_json()))
    else:
        print(json.dumps({"error": f"Unknown command: {argv[1]}"}))
    sys.stdout.flush()

if __name__ == "__main__":
    main()



"""
Plan for Course Models (add to api/models/ directory):

from datetime import datetime
from typing import Optional, List
from server.api.models._base import Model

class Semester(Model):
    code: str  # e.g., "1222"
    name: str  # e.g., "Spring 2022"
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Course(Model):
    course_id: str
    catalog_number: str
    title: str
    description: Optional[str] = None
    semester_code: str
    subject_code: str  # e.g., "COS"
    pdf_required: bool = False
    pdf_permitted: bool = True
    audit: bool = True
    grading: List[dict] = []
    assignments: Optional[str] = None
    prerequisites: Optional[str] = None
    distribution_area: Optional[str] = None
    website: Optional[str] = None


add course endpoints to handle imported data 

Create import script that calls studentapp.py, processes JSON response, and stores in MongoDB
Similar to https://github.com/TigerAppsOrg/PrincetonCourses/blob/master/importers/importBasicCourseDetails.js 
but need to make for own setup

"""
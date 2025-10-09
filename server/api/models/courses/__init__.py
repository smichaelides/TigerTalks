from typing import Optional, List, Dict, Any
from api.models._base import Model


class Reading(Model):
    title: str
    author: Optional[str] = None


class Crosslisting(Model):
    department: str
    catalog_number: str


class PDF(Model):
    permitted: bool
    required: bool


class Course(Model):
    course_id: str
    catalog_number: str
    title: str
    semester: int  # References Semester._id
    readings: List[Reading] = []
    department: str
    description: Optional[str] = None
    classes: List[Dict[str, Any]] = []
    instructors: List[int] = []  # References Instructor._id
    crosslistings: List[Crosslisting] = []
    distribution: Optional[str] = None
    pdf: PDF = PDF(permitted=True, required=False)
    audit: bool = True
    assignments: List[str] = []
    reading_amount: Optional[int] = None
    grading: List[Dict[str, Any]] = []
    reserved_seats: List[str] = []
    prerequisites: Optional[str] = None
    open: bool = True
    equivalent_courses: Optional[str] = None
    other_information: Optional[str] = None
    other_requirements: Optional[str] = None
    website: Optional[str] = None
    track: Optional[str] = None
    new: bool = False

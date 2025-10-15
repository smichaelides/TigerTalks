from typing import List, Optional
from pydantic import BaseModel


class Building(BaseModel):
    location_code: str
    name: str


class Meeting(BaseModel):
    meeting_number: str
    start_time: str
    end_time: str
    room: str
    days: List[str]
    building: Building


class Schedule(BaseModel):
    start_date: str
    end_date: str
    meetings: List[Meeting]


class ClassSection(BaseModel):
    class_number: str
    section: str
    status: str
    pu_calc_status: str
    seat_status: str
    type_name: str
    capacity: str
    enrollment: str
    schedule: Schedule


class Instructor(BaseModel):
    emplid: str
    first_name: str
    last_name: str
    full_name: str


class Crosslisting(BaseModel):
    subject: str
    catalog_number: str


class Detail(BaseModel):
    start_date: str
    end_date: str
    track: str
    description: str
    seat_reservations: str


class PDF(BaseModel):
    required: bool
    permitted: bool


class GradingComponent(BaseModel):
    component: str
    weight: float


class Course(BaseModel):
    # Core identifiers
    guid: Optional[str] = None
    course_id: str
    catalog_number: str
    title: str
    semester: int
    department: str

    # Description & metadata
    description: Optional[str] = None
    detail: Optional[Detail] = None
    pdf: PDF
    audit: bool
    grading: List[GradingComponent]
    assignments: str
    reserved_seats: List[str]
    readings: List[str]
    prerequisites: str
    other_information: str
    other_requirements: str
    website: str
    distribution: str
    open: bool
    new: bool

    # Additional nested lists
    instructors: Optional[List[Instructor]] = None
    crosslistings: Optional[List[Crosslisting]] = None
    classes: Optional[List[ClassSection]] = None

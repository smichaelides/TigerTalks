from typing import Optional
from api.models._base import Model


class Semester(Model):
    code: int  # e.g., 1222 for Spring 2022
    name: str  # e.g., "Spring 2022"
    start_date: Optional[str] = None
    end_date: Optional[str] = None

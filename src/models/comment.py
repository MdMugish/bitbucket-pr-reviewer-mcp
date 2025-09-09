from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SeverityLevel(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    SUMMARY = "SUMMARY"


class Comment(BaseModel):
    content: str
    severity: SeverityLevel
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    is_summary: bool = False

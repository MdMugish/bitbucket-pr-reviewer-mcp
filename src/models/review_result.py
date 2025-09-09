from typing import List
from pydantic import BaseModel
from .comment import Comment


class ReviewResult(BaseModel):
    pr_id: str
    comments: List[Comment]
    summary: str
    total_issues: int
    critical_issues: int

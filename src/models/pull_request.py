from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PullRequest(BaseModel):
    id: str
    title: str
    description: str
    author: str
    status: str
    repository: str
    created_at: datetime
    updated_at: datetime
    source_branch: Optional[str] = None
    destination_branch: Optional[str] = None

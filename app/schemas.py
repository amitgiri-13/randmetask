from pydantic import BaseModel
from typing import List

class TaskAssignmentRequest(BaseModel):
    tasks: List[str]
    members: List[str]
    
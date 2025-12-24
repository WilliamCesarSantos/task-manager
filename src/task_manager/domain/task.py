from dataclasses import dataclass
from datetime import date
from typing import Optional

OPEN = "OPEN"
CLOSED = "CLOSED"

@dataclass
class Task:
    id: Optional[int]
    description: str
    due_date: date
    status: str = OPEN

    def close(self):
        self.status = CLOSED

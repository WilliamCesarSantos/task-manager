from dataclasses import dataclass
from datetime import date

OPEN = "OPEN"
CLOSED = "CLOSED"

@dataclass
class Task:
    id: int
    description: str
    due_date: date
    status: str = OPEN

    def close(self):
        self.status = CLOSED

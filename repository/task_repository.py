import json
from datetime import date
from pathlib import Path
from domain.task import Task

DATA_FILE = Path("data/tasks.json")


class TaskRepository:

    def __init__(self):
        DATA_FILE.parent.mkdir(exist_ok=True)
        if not DATA_FILE.exists():
            self._save([])

    def find_all(self):
        return self._load()

    def save(self, task: Task):
        tasks = self._load()
        tasks.append(task)
        self._save(tasks)

    def update(self, task: Task):
        tasks = self._load()
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
        self._save(tasks)

    def delete(self, task_id: int):
        tasks = [t for t in self._load() if t.id != task_id]
        self._save(tasks)

    def _load(self):
        with open(DATA_FILE, "r") as file:
            raw_tasks = json.load(file)
            return [
                Task(
                    id=t["id"],
                    description=t["description"],
                    due_date=date.fromisoformat(t["due_date"]),
                    status=t["status"]
                )
                for t in raw_tasks
            ]

    def _save(self, tasks):
        with open(DATA_FILE, "w") as file:
            json.dump(
                [
                    {
                        "id": t.id,
                        "description": t.description,
                        "due_date": t.due_date.isoformat(),
                        "status": t.status
                    }
                    for t in tasks
                ],
                file,
                indent=2
            )

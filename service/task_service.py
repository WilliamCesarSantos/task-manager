from datetime import date
from domain.task import Task
from repository.task_repository import TaskRepository


class TaskService:

    def __init__(self):
        self.repository = TaskRepository()

    def list_tasks(self):
        return self.repository.find_all()

    def add_task(self, description: str, due_date: date):
        tasks = self.repository.find_all()
        new_id = max([t.id for t in tasks], default=0) + 1
        task = Task(new_id, description, due_date)
        self.repository.save(task)

    def edit_task(self, task_id: int, description: str, due_date: date):
        tasks = self.repository.find_all()
        for task in tasks:
            if task.id == task_id:
                task.description = description
                task.due_date = due_date
                self.repository.update(task)

    def complete_task(self, task_id: int):
        tasks = self.repository.find_all()
        for task in tasks:
            if task.id == task_id:
                task.close()
                self.repository.update(task)

    def delete_task(self, task_id: int):
        self.repository.delete(task_id)

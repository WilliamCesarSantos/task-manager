from typing import Optional
from datetime import date
from task_manager.domain.task import Task
from task_manager.repository.task_repository_interface import TaskRepositoryInterface


class TaskService:

    def __init__(self, repository: TaskRepositoryInterface):
        self.repository = repository

    def list_tasks(self):
        return self.repository.find_all()

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.repository.find_by_id(task_id)

    def add_task(self, description: str, due_date: date) -> Task:
        task = Task(None, description, due_date)
        self.repository.save(task)
        return task

    def edit_task(self, task_id: int, description: str, due_date: date) -> Optional[Task]:
        task = self.repository.find_by_id(task_id)
        if task:
            task.description = description
            task.due_date = due_date
            self.repository.update(task)
            return task
        return None

    def complete_task(self, task_id: int) -> Optional[Task]:
        task = self.repository.find_by_id(task_id)
        if task:
            task.close()
            self.repository.update(task)
            return task
        return None

    def delete_task(self, task_id: int) -> Optional[Task]:
        task = self.repository.find_by_id(task_id)
        if task:
            self.repository.delete(task_id)
            return task
        return None

from abc import ABC, abstractmethod
from typing import List, Optional
from task_manager.domain.task import Task

class TaskRepositoryInterface(ABC):
    
    @abstractmethod
    def find_all(self) -> List[Task]:
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        pass

from datetime import date
from src.task_manager.domain.task import Task, OPEN, CLOSED

def test_create_task():
    due_date = date(2023, 12, 31)
    task = Task(id=1, description="Test Task", due_date=due_date)
    
    assert task.id == 1
    assert task.description == "Test Task"
    assert task.due_date == due_date
    assert task.status == OPEN

def test_close_task():
    task = Task(id=1, description="Test Task", due_date=date.today())
    task.close()
    
    assert task.status == CLOSED

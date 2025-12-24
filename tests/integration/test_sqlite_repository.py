import pytest
import sqlite3
from datetime import date
from pathlib import Path
from task_manager.domain.task import Task, OPEN, CLOSED
from task_manager.repository.sqlite_task_repository import SQLiteTaskRepository

# Use an in-memory database for testing to avoid file I/O and cleanup issues
TEST_DB_PATH = Path(":memory:")

@pytest.fixture
def repository():
    # Initialize repository with in-memory database
    repo = SQLiteTaskRepository(TEST_DB_PATH)
    return repo

def test_save_and_find_by_id(repository):
    task = Task(id=None, description="Test Task", due_date=date(2023, 12, 31))
    
    repository.save(task)
    
    assert task.id is not None
    
    fetched_task = repository.find_by_id(task.id)
    assert fetched_task is not None
    assert fetched_task.id == task.id
    assert fetched_task.description == "Test Task"
    assert fetched_task.due_date == date(2023, 12, 31)
    assert fetched_task.status == OPEN

def test_find_all(repository):
    task1 = Task(id=None, description="Task 1", due_date=date.today())
    task2 = Task(id=None, description="Task 2", due_date=date.today())
    
    repository.save(task1)
    repository.save(task2)
    
    tasks = repository.find_all()
    
    assert len(tasks) == 2
    assert any(t.id == task1.id for t in tasks)
    assert any(t.id == task2.id for t in tasks)

def test_update(repository):
    task = Task(id=None, description="Original", due_date=date.today())
    repository.save(task)
    
    task.description = "Updated"
    task.status = CLOSED
    repository.update(task)
    
    updated_task = repository.find_by_id(task.id)
    assert updated_task.description == "Updated"
    assert updated_task.status == CLOSED

def test_delete(repository):
    task = Task(id=None, description="To Delete", due_date=date.today())
    repository.save(task)
    
    repository.delete(task.id)
    
    assert repository.find_by_id(task.id) is None

def test_find_by_id_not_found(repository):
    assert repository.find_by_id(999) is None

import pytest
from datetime import date
from unittest.mock import Mock
from task_manager.domain.task import Task, OPEN, CLOSED
from task_manager.service.task_service import TaskService
from task_manager.repository.task_repository_interface import TaskRepositoryInterface

@pytest.fixture
def mock_repository():
    return Mock(spec=TaskRepositoryInterface)

@pytest.fixture
def task_service(mock_repository):
    # Dependency Injection in action
    return TaskService(mock_repository)

def test_list_tasks(task_service, mock_repository):
    expected_tasks = [
        Task(id=1, description="Task 1", due_date=date.today()),
        Task(id=2, description="Task 2", due_date=date.today())
    ]
    mock_repository.find_all.return_value = expected_tasks
    
    tasks = task_service.list_tasks()
    
    assert tasks == expected_tasks
    mock_repository.find_all.assert_called_once()

def test_add_task(task_service, mock_repository):
    description = "New Task"
    due_date = date(2023, 12, 31)
    
    task_service.add_task(description, due_date)
    
    mock_repository.save.assert_called_once()
    saved_task = mock_repository.save.call_args[0][0]
    assert saved_task.description == description
    assert saved_task.due_date == due_date
    assert saved_task.id is None
    assert saved_task.status == OPEN

def test_edit_task_existing(task_service, mock_repository):
    task_id = 1
    original_task = Task(id=task_id, description="Old", due_date=date.today())
    mock_repository.find_by_id.return_value = original_task
    
    new_desc = "Updated"
    new_date = date(2024, 1, 1)
    
    task_service.edit_task(task_id, new_desc, new_date)
    
    mock_repository.find_by_id.assert_called_with(task_id)
    mock_repository.update.assert_called_once_with(original_task)
    assert original_task.description == new_desc
    assert original_task.due_date == new_date

def test_edit_task_not_found(task_service, mock_repository):
    mock_repository.find_by_id.return_value = None
    
    task_service.edit_task(999, "Desc", date.today())
    
    mock_repository.find_by_id.assert_called_with(999)
    mock_repository.update.assert_not_called()

def test_complete_task(task_service, mock_repository):
    task_id = 1
    task = Task(id=task_id, description="Task", due_date=date.today())
    mock_repository.find_by_id.return_value = task
    
    task_service.complete_task(task_id)
    
    assert task.status == CLOSED
    mock_repository.update.assert_called_once_with(task)

def test_delete_task(task_service, mock_repository):
    task_id = 1
    task_service.delete_task(task_id)
    mock_repository.delete.assert_called_once_with(task_id)

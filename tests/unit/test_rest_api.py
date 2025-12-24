import pytest
from datetime import date
from unittest.mock import Mock
from task_manager.domain.task import Task, OPEN, CLOSED
from task_manager.rest_api.rest_api import create_app
from task_manager.service.task_service import TaskService

@pytest.fixture
def mock_service():
    return Mock(spec=TaskService)

@pytest.fixture
def client(mock_service):
    # Create app with mocked service
    app = create_app(mock_service)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_list_tasks(client, mock_service):
    mock_service.list_tasks.return_value = [
        Task(id=1, description="Task 1", due_date=date(2023, 12, 31), status=OPEN)
    ]
    
    response = client.get('/task-manager/tasks')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['description'] == "Task 1"
    assert data[0]['due_date'] == "2023-12-31"
    assert data[0]['status'] == OPEN

def test_add_task_success(client, mock_service):
    payload = {
        "description": "New Task",
        "due_date": "2023-12-31"
    }
    
    response = client.post('/task-manager/tasks', json=payload)
    
    assert response.status_code == 201
    assert response.get_json() == {"message": "Task created successfully"}
    mock_service.add_task.assert_called_once_with("New Task", date(2023, 12, 31))

def test_add_task_missing_fields(client, mock_service):
    payload = {"description": "Incomplete"}
    
    response = client.post('/task-manager/tasks', json=payload)
    
    assert response.status_code == 400
    assert "error" in response.get_json()
    mock_service.add_task.assert_not_called()

def test_add_task_invalid_date(client, mock_service):
    payload = {
        "description": "Task",
        "due_date": "invalid-date"
    }
    
    response = client.post('/task-manager/tasks', json=payload)
    
    assert response.status_code == 400
    assert "Invalid date format" in response.get_json()['error']
    mock_service.add_task.assert_not_called()

def test_edit_task_success(client, mock_service):
    task_id = 1
    payload = {
        "description": "Updated Task",
        "due_date": "2024-01-01"
    }
    
    response = client.put(f'/task-manager/tasks/{task_id}', json=payload)
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Task updated successfully"}
    mock_service.edit_task.assert_called_once_with(task_id, "Updated Task", date(2024, 1, 1))

def test_complete_task(client, mock_service):
    task_id = 1
    
    response = client.patch(f'/task-manager/tasks/{task_id}/complete')
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Task completed successfully"}
    mock_service.complete_task.assert_called_once_with(task_id)

def test_delete_task(client, mock_service):
    task_id = 1
    
    response = client.delete(f'/task-manager/tasks/{task_id}')
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Task deleted successfully"}
    mock_service.delete_task.assert_called_once_with(task_id)

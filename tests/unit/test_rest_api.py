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

def test_get_task_success(client, mock_service):
    task_id = 1
    task = Task(id=task_id, description="Task 1", due_date=date(2023, 12, 31), status=OPEN)
    mock_service.get_task.return_value = task
    
    response = client.get(f'/task-manager/tasks/{task_id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == task_id
    assert data['description'] == "Task 1"
    assert data['due_date'] == "2023-12-31"
    assert data['status'] == OPEN
    
    mock_service.get_task.assert_called_once_with(task_id)

def test_get_task_not_found(client, mock_service):
    task_id = 999
    mock_service.get_task.return_value = None
    
    response = client.get(f'/task-manager/tasks/{task_id}')
    
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}
    
    mock_service.get_task.assert_called_once_with(task_id)

def test_add_task_success(client, mock_service):
    payload = {
        "description": "New Task",
        "due_date": "2023-12-31"
    }
    
    created_task = Task(id=1, description="New Task", due_date=date(2023, 12, 31), status=OPEN)
    mock_service.add_task.return_value = created_task
    
    response = client.post('/task-manager/tasks', json=payload)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['description'] == "New Task"
    assert data['due_date'] == "2023-12-31"
    assert data['status'] == OPEN

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
    
    updated_task = Task(id=task_id, description="Updated Task", due_date=date(2024, 1, 1), status=OPEN)
    mock_service.edit_task.return_value = updated_task
    
    response = client.put(f'/task-manager/tasks/{task_id}', json=payload)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == task_id
    assert data['description'] == "Updated Task"
    assert data['due_date'] == "2024-01-01"
    
    mock_service.edit_task.assert_called_once_with(task_id, "Updated Task", date(2024, 1, 1))

def test_edit_task_not_found(client, mock_service):
    task_id = 999
    payload = {
        "description": "Updated Task",
        "due_date": "2024-01-01"
    }
    
    mock_service.edit_task.return_value = None
    
    response = client.put(f'/task-manager/tasks/{task_id}', json=payload)
    
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}

def test_complete_task(client, mock_service):
    task_id = 1
    completed_task = Task(id=task_id, description="Task", due_date=date.today(), status=CLOSED)
    mock_service.complete_task.return_value = completed_task
    
    response = client.patch(f'/task-manager/tasks/{task_id}/complete')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == task_id
    assert data['status'] == CLOSED
    
    mock_service.complete_task.assert_called_once_with(task_id)

def test_complete_task_not_found(client, mock_service):
    task_id = 999
    mock_service.complete_task.return_value = None
    
    response = client.patch(f'/task-manager/tasks/{task_id}/complete')
    
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}

def test_delete_task(client, mock_service):
    task_id = 1
    deleted_task = Task(id=task_id, description="Task", due_date=date.today(), status=OPEN)
    mock_service.delete_task.return_value = deleted_task
    
    response = client.delete(f'/task-manager/tasks/{task_id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == task_id
    
    mock_service.delete_task.assert_called_once_with(task_id)

def test_delete_task_not_found(client, mock_service):
    task_id = 999
    mock_service.delete_task.return_value = None
    
    response = client.delete(f'/task-manager/tasks/{task_id}')
    
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}

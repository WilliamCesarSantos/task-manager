import pytest
from datetime import date
from unittest.mock import Mock, patch, call
from task_manager.domain.task import Task, OPEN
from task_manager.ui.console_menu import ConsoleMenu
from task_manager.service.task_service import TaskService

@pytest.fixture
def mock_service():
    return Mock(spec=TaskService)

@pytest.fixture
def console_menu(mock_service):
    # Dependency Injection in action
    return ConsoleMenu(mock_service)

def test_show_exit(console_menu):
    with patch('builtins.input', return_value="0"), \
         patch('builtins.print') as mock_print:
        console_menu.show()
        # Should exit immediately
        assert mock_print.call_count >= 1 # Menu is printed at least once

def test_list_tasks(console_menu, mock_service):
    mock_service.list_tasks.return_value = [
        Task(id=1, description="Task 1", due_date=date(2023, 12, 31), status=OPEN)
    ]
    
    # Simulate choosing option 1 then 0 (exit)
    with patch('builtins.input', side_effect=["1", "0"]), \
         patch('builtins.print') as mock_print:
        console_menu.show()
        
        mock_service.list_tasks.assert_called_once()
        # Verify output contains task info
        printed_content = [call[0][0] for call in mock_print.call_args_list if call.args]
        assert any("[1] Task 1" in str(s) for s in printed_content)

def test_add_task(console_menu, mock_service):
    # Simulate option 4, description, date, then exit
    inputs = ["4", "New Task", "2023-12-31", "0"]
    
    with patch('builtins.input', side_effect=inputs):
        console_menu.show()
        
        mock_service.add_task.assert_called_once_with("New Task", date(2023, 12, 31))

def test_edit_task(console_menu, mock_service):
    # Simulate option 2, id, description, date, then exit
    inputs = ["2", "1", "Updated Task", "2024-01-01", "0"]
    
    with patch('builtins.input', side_effect=inputs):
        console_menu.show()
        
        mock_service.edit_task.assert_called_once_with(1, "Updated Task", date(2024, 1, 1))

def test_complete_task(console_menu, mock_service):
    # Simulate option 5, id, then exit
    inputs = ["5", "1", "0"]
    
    with patch('builtins.input', side_effect=inputs):
        console_menu.show()
        
        mock_service.complete_task.assert_called_once_with(1)

def test_delete_task(console_menu, mock_service):
    # Simulate option 3, id, then exit
    inputs = ["3", "1", "0"]
    
    with patch('builtins.input', side_effect=inputs):
        console_menu.show()
        
        mock_service.delete_task.assert_called_once_with(1)

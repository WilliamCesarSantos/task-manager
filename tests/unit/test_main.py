import sys
from unittest.mock import patch, MagicMock
from task_manager.main import main, REST_API, CONSOLE

def test_main_default_rest_api():
    with patch.object(sys, 'argv', ['main.py']), \
         patch('task_manager.main.create_app') as mock_create_app, \
         patch('task_manager.main.ConsoleMenu') as mock_console, \
         patch('task_manager.main.SQLiteTaskRepository') as mock_repo, \
         patch('task_manager.main.TaskService') as mock_service:
        
        mock_app = mock_create_app.return_value
        
        main()
        
        mock_create_app.assert_called_once()
        mock_app.run.assert_called_once_with(debug=True)
        mock_console.assert_not_called()

def test_main_explicit_rest_api():
    with patch.object(sys, 'argv', ['main.py', 'REST_API']), \
         patch('task_manager.main.create_app') as mock_create_app, \
         patch('task_manager.main.ConsoleMenu') as mock_console, \
         patch('task_manager.main.SQLiteTaskRepository') as mock_repo, \
         patch('task_manager.main.TaskService') as mock_service:
        
        mock_app = mock_create_app.return_value
        
        main()
        
        mock_create_app.assert_called_once()
        mock_app.run.assert_called_once_with(debug=True)
        mock_console.assert_not_called()

def test_main_console():
    with patch.object(sys, 'argv', ['main.py', 'CONSOLE']), \
         patch('task_manager.main.create_app') as mock_create_app, \
         patch('task_manager.main.ConsoleMenu') as mock_console, \
         patch('task_manager.main.SQLiteTaskRepository') as mock_repo, \
         patch('task_manager.main.TaskService') as mock_service:
        
        mock_console_instance = mock_console.return_value
        
        main()
        
        mock_console_instance.show.assert_called_once()
        mock_create_app.assert_not_called()

def test_main_invalid_arg_defaults_to_rest_api():
    with patch.object(sys, 'argv', ['main.py', 'INVALID_ARG']), \
         patch('task_manager.main.create_app') as mock_create_app, \
         patch('task_manager.main.ConsoleMenu') as mock_console, \
         patch('task_manager.main.SQLiteTaskRepository') as mock_repo, \
         patch('task_manager.main.TaskService') as mock_service:
        
        mock_app = mock_create_app.return_value
        
        main()
        
        mock_create_app.assert_called_once()
        mock_app.run.assert_called_once_with(debug=True)
        mock_console.assert_not_called()

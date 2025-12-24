import sys
from task_manager.repository.sqlite_task_repository import SQLiteTaskRepository
from task_manager.service.task_service import TaskService
from task_manager.ui.console_menu import ConsoleMenu
from task_manager.rest_api.rest_api import create_app

REST_API = "REST_API"
CONSOLE = "CONSOLE"

def main():
    # Composition Root: Create dependencies
    repository = SQLiteTaskRepository()
    service = TaskService(repository)

    interface_type = REST_API
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        if arg in [REST_API, CONSOLE]:
            interface_type = arg

    if interface_type == CONSOLE:
        # Inject service into UI
        ConsoleMenu(service).show()
    else:
        # Inject service into API
        app = create_app(service)
        app.run(debug=True)

if __name__ == "__main__":
    main()

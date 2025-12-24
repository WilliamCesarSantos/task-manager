from flask import Flask, request, jsonify
from datetime import date
from task_manager.service.task_service import TaskService

def create_app(service: TaskService):
    app = Flask(__name__)
    BASE_URL = "/task-manager"

    @app.route(f"{BASE_URL}/tasks", methods=["GET"])
    def list_tasks():
        tasks = service.list_tasks()
        return jsonify([
            {
                "id": t.id,
                "description": t.description,
                "due_date": t.due_date.isoformat(),
                "status": t.status
            }
            for t in tasks
        ])

    @app.route(f"{BASE_URL}/tasks", methods=["POST"])
    def add_task():
        data = request.json
        description = data.get("description")
        due_date_str = data.get("due_date")
        
        if not description or not due_date_str:
            return jsonify({"error": "Description and due_date are required"}), 400
            
        try:
            due_date = date.fromisoformat(due_date_str)
            service.add_task(description, due_date)
            return jsonify({"message": "Task created successfully"}), 201
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    @app.route(f"{BASE_URL}/tasks/<int:task_id>", methods=["PUT"])
    def edit_task(task_id):
        data = request.json
        description = data.get("description")
        due_date_str = data.get("due_date")
        
        if not description or not due_date_str:
            return jsonify({"error": "Description and due_date are required"}), 400

        try:
            due_date = date.fromisoformat(due_date_str)
            service.edit_task(task_id, description, due_date)
            return jsonify({"message": "Task updated successfully"})
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    @app.route(f"{BASE_URL}/tasks/<int:task_id>/complete", methods=["PATCH"])
    def complete_task(task_id):
        service.complete_task(task_id)
        return jsonify({"message": "Task completed successfully"})

    @app.route(f"{BASE_URL}/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        service.delete_task(task_id)
        return jsonify({"message": "Task deleted successfully"})
    
    return app

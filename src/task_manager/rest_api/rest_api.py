from flask import Flask, request, jsonify
from datetime import date
from task_manager.service.task_service import TaskService
from task_manager.domain.task import Task

def create_app(service: TaskService):
    app = Flask(__name__)
    BASE_URL = "/task-manager"

    def task_to_dict(task: Task):
        return {
            "id": task.id,
            "description": task.description,
            "due_date": task.due_date.isoformat(),
            "status": task.status
        }

    def handle_task_response(task: Task, status_code=200):
        if task:
            return jsonify(task_to_dict(task)), status_code
        return jsonify({"error": "Task not found"}), 404

    @app.route(f"{BASE_URL}/tasks", methods=["GET"])
    def list_tasks():
        tasks = service.list_tasks()
        return jsonify([task_to_dict(t) for t in tasks])

    @app.route(f"{BASE_URL}/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        return handle_task_response(service.get_task(task_id))

    @app.route(f"{BASE_URL}/tasks", methods=["POST"])
    def add_task():
        data = request.json
        description = data.get("description")
        due_date_str = data.get("due_date")
        
        if not description or not due_date_str:
            return jsonify({"error": "Description and due_date are required"}), 400
            
        try:
            due_date = date.fromisoformat(due_date_str)
            created_task = service.add_task(description, due_date)
            return handle_task_response(created_task, 201)
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
            updated_task = service.edit_task(task_id, description, due_date)
            return handle_task_response(updated_task)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    @app.route(f"{BASE_URL}/tasks/<int:task_id>/complete", methods=["PATCH"])
    def complete_task(task_id):
        return handle_task_response(service.complete_task(task_id))

    @app.route(f"{BASE_URL}/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        return handle_task_response(service.delete_task(task_id))
    
    return app

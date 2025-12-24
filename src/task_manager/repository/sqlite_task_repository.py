import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional, List
from task_manager.domain.task import Task
from task_manager.repository.task_repository_interface import TaskRepositoryInterface

DEFAULT_DB_FILE = Path("../data/tasks.db")


class SQLiteTaskRepository(TaskRepositoryInterface):

    def __init__(self, db_path: Path = DEFAULT_DB_FILE):
        self._ensure_db_directory(db_path)
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def find_all(self) -> List[Task]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, description, due_date, status FROM tasks")
        return [self._to_task(row) for row in cursor.fetchall()]

    def find_by_id(self, task_id: int) -> Optional[Task]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, description, due_date, status FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return self._to_task(row) if row else None

    def save(self, task: Task) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (description, due_date, status) VALUES (?, ?, ?)",
            (task.description, task.due_date.isoformat(), task.status)
        )
        self.connection.commit()
        task.id = cursor.lastrowid

    def update(self, task: Task) -> None:
        self._execute(
            "UPDATE tasks SET description = ?, due_date = ?, status = ? WHERE id = ?",
            (task.description, task.due_date.isoformat(), task.status, task.id)
        )

    def delete(self, task_id: int) -> None:
        self._execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def _create_table(self) -> None:
        self._execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

    def _execute(self, sql: str, params: tuple = ()) -> None:
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()

    def _to_task(self, row: tuple) -> Task:
        return Task(
            id=row[0],
            description=row[1],
            due_date=date.fromisoformat(row[2]),
            status=row[3]
        )

    def _ensure_db_directory(self, db_path: Path) -> None:
        if not db_path.parent.exists():
            db_path.parent.mkdir(parents=True, exist_ok=True)
